from __future__ import print_function

import os
import shutil

import pandas as pd
from thefuzz import process
from typeform import get_field_from_item, get_responses
from util import naive_postcode_formatter, write_csv
from util.date import round_to_nearest_hour

working_dir = os.path.join('working')
working_file = os.path.join(working_dir, 'roadshow_attendees.csv')

output_dir = os.path.join('data', 'metrics', 'roadshow_attendees')
attendees_file = os.path.join(output_dir, 'attendees.csv')
site_dir = os.path.join('docs', '_data', 'metrics', 'roadshow_attendees')


def load_postcodes():
    return pd.read_csv(os.path.join('data', 'reference', 'postcodes.csv'))


def load_wards_2021():
    return pd.read_csv(os.path.join('data', 'reference', 'Wards_(December_2021)_GB_BFC.csv'))


def load_constituencies_2020():
    return pd.read_csv(os.path.join('data', 'reference', 'Westminster_Parliamentary_Constituencies_(December_2020)_UK_BFC.csv'))


def get_workshop_responses():
    form_id = 'vm2OxH3L'
    postcode_field_id = 'GHOzEy9LwD8o'
    workshop_data = get_responses(form_id, fields=postcode_field_id)

    def get_time_and_postcode(item):
        postcode = get_field_from_item(
            item, postcode_field_id)
        return {
            'datetime': item['submitted_at'],
            'postcode': naive_postcode_formatter(postcode)
        }

    data = [get_time_and_postcode(x) for x in workshop_data['items']]

    write_csv(data, working_file,
              field_names=['datetime', 'postcode'])


def summarise():
    data = pd.read_csv(working_file)
    data['datetime'] = pd.to_datetime(data['datetime']).dt.round(freq='D')

    os.makedirs(output_dir, exist_ok=True)

    attendees = pd.read_csv(attendees_file)
    attendees.rename(columns={ 'date': 'datetime' }, inplace=True)
    attendees['datetime'] = pd.to_datetime(attendees['datetime'], utc=True)

    attendees_summary = attendees.groupby(by='datetime').sum()

    summary = data.groupby(by='datetime').count()
    summary = pd.DataFrame({
        'responses': summary.postcode
    })

    summary = pd.concat([attendees_summary, summary]).groupby('datetime').sum().astype(int)
    summary.index.names=['date']
    summary.to_csv(os.path.join(output_dir, 'summary.csv'),
      date_format='%Y-%m-%d')

    pc = load_postcodes()

    # Normalise names
    data.postcode = data.postcode.str.upper().str.replace(r'\s+', '', regex=True)
    pc['postcode'] = pc.pcds.str.upper().str.replace(r'\s+', '', regex=True)

    counts = data.postcode.value_counts().to_frame(name='responses')
    counts = counts.merge(pc, left_index=True, right_on='postcode')

    responses_by_ward = pd.DataFrame({
      'wd21cd': counts.osward,
      'responses': counts.responses,
    })
    attendees_by_ward = pd.DataFrame({
      'wd21cd': attendees.wd21cd,
      'attendees': attendees.attendees
    })
    wards = load_wards_2021()
    by_ward = pd.merge(
      left = pd.concat([attendees_by_ward, responses_by_ward]).groupby('wd21cd').sum(),
      right = wards,
      left_index=True,
      right_on='WD21CD',
    )

    pd.DataFrame({
        'ward_name': by_ward.WD21NM,
        'ward_code': by_ward.WD21CD,
        'attendees': by_ward.attendees.astype(int),
        'responses': by_ward.responses.astype(int),
    }).to_csv(os.path.join(output_dir, 'count_by_ward.csv'), index=False)

    cons = load_constituencies_2020()
    by_pcon = counts.groupby('pcon').responses \
        .sum().to_frame() \
        .merge(cons, left_index=True, right_on='PCON20CD', how='left')
    pd.DataFrame({
        'constituency_name': by_pcon.PCON20NM,
        'constituency_code': by_pcon.PCON20CD,
        'responses': by_pcon.responses,
    }).to_csv(os.path.join(output_dir, 'count_by_constituency.csv'), index=False)


def process_workshop_attendees(freq='D'):
    data = pd.read_csv(os.path.join(output_dir, 'summary.csv'),
                       parse_dates=['date'])
    # Summarises by required frequency and fills in gaps
    data = data.resample('W-Fri', on='date').sum().reset_index()

    data.rename(columns={
        'date': 'week_ending'
    }, inplace=True)

    data = pd.concat([
        data,
        pd.DataFrame.from_records([{
            'week_ending': data.week_ending.min() - pd.Timedelta(weeks=1),
            'attendees': 0,
            'responses': 0
        }])
    ]).sort_values('week_ending')

    data['cumulative_attendees'] = data.attendees.cumsum()
    data['cumulative_responses'] = data.responses.cumsum()

    data.to_csv(os.path.join(site_dir, 'summary.csv'),
                date_format="%Y-%m-%d", index=False)

    shutil.copy(os.path.join(output_dir, 'count_by_ward.csv'),
                os.path.join(site_dir, 'by_ward.csv'))


def process_attendees_spreadsheet():
    wards = load_wards_2021()
    # Remove more southerly wards
    wards = wards.drop(wards[wards['LAT'] < 52].index)
    wards = pd.DataFrame({
      'wd21cd': wards.WD21CD,
      'wd21nm': wards.WD21NM
    })

    data = pd.read_excel(
        './working/Leeds 2023 Roadshow Open Innovations.xlsx', sheet_name='Sheet1')
    data.columns = ['ward', 'date', 'attendees']
    data = data.dropna()
    data['wd21nm'] = data.ward.apply(
        lambda x: process.extractOne(x, wards.wd21nm)[0])
    data = pd.merge(left=data, right=wards, on='wd21nm')
    data = pd.DataFrame({
      'wd21nm': data.wd21nm,
      'wd21cd': data.wd21cd,
      'date': data.date,
      'attendees': data.attendees
    })
    data = data.sort_values(by='date')
    data.to_csv(attendees_file, index=False)
    
