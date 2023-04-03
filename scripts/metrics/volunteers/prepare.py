import os

import pandas as pd
from metrics.volunteers.data import load_raw_data
from metrics.volunteers.setup import VIEW_DIR
from metrics.volunteers.summarise import (summarise_by_local_authority,
                                          summarise_by_ward, summarise_by_week)
from metrics.volunteers.transform_shifts import SHIFT_DATA


def summarise():
    data = load_raw_data()
    data = data[data.current == True]
    print(data)
    summarise_by_ward(data, os.path.join(VIEW_DIR, 'by_ward.csv'))
    summarise_by_week(data, os.path.join(VIEW_DIR, 'by_week.csv'))
    summarise_by_local_authority(data, os.path.join(VIEW_DIR, 'by_local_authority.csv'), os.path.join(
        VIEW_DIR, 'la_stats.json'), os.path.join(VIEW_DIR, 'west_yorkshire.csv'))


def prepare_shift_data():
    os.makedirs(os.path.join(VIEW_DIR, 'shifts'), exist_ok=True)

    shifts = pd.read_csv(SHIFT_DATA, parse_dates=['date']).rename(columns={
        'attended': 'volunteer_shifts',
      })
    shifts.event_type = shifts.event_type.fillna(
        'volunteer_event_programme'
      ).map(
        lambda x: x.lower().replace(' ', '_')
      )

    grouped = shifts[~shifts.event_type.isin([
        'volunteer_event_programme'
    ])][[
        'date',
        'volunteer_shifts',
        'volunteer_hours',
    ]].groupby('date')

    by_week = grouped.sum().resample('W-FRI').sum().round().astype(int)
    by_week['cumulative_volunteer_shifts'] = by_week.volunteer_shifts.cumsum()
    by_week['cumulative_volunteer_hours'] = by_week.volunteer_hours.cumsum()
    by_week.to_csv(os.path.join(VIEW_DIR, 'shifts', 'by_week.csv'))

    summary = shifts[[
        'event_type',
        'volunteer_shifts',
        'volunteer_hours'
    ]]
    summary = summary.groupby('event_type').sum().round().astype(int)
    summary.loc['total'] = summary.sum()
    summary.loc['total_events'] = summary[summary.index.isin(['leeds_2023_events', 'partner_events'])].sum()
    summary.transpose().to_json(os.path.join(VIEW_DIR, 'shifts',
                    'summary.json'), orient="index", indent=2)


if __name__ == "__main__":
    summarise()
    prepare_shift_data()
