import os

import pandas as pd
from metrics.volunteers.data import load_raw_data
from metrics.volunteers.setup import VIEW_DIR
from metrics.volunteers.summarise import (summarise_by_local_authority,
                                          summarise_by_ward, summarise_by_week)
from metrics.volunteers.transform_shifts import SHIFT_DATA


def summarise():
    data = load_raw_data()
    summarise_by_ward(data, os.path.join(VIEW_DIR, 'by_ward.csv'))
    summarise_by_week(data, os.path.join(VIEW_DIR, 'by_week.csv'))
    summarise_by_local_authority(data, os.path.join(VIEW_DIR, 'by_local_authority.csv'), os.path.join(
        VIEW_DIR, 'la_stats.json'), os.path.join(VIEW_DIR, 'west_yorkshire.csv'))


def prepare_shift_data():
    shifts = pd.read_csv(SHIFT_DATA, parse_dates=['date'])

    grouped = shifts.groupby('date')
    by_week = pd.DataFrame({
        'volunteers': grouped.attended.sum(),
        'hours': grouped.volunteer_hours.sum(),
    }).resample('W-FRI').sum().round().astype(int).reset_index()
    by_week.to_csv(os.path.join(VIEW_DIR, 'shifts_by_week.csv'), index=False)


if __name__ == "__main__":
    summarise()
    prepare_shift_data()
