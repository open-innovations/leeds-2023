from __future__ import print_function
import os
from typeform import get_responses, get_field_from_item
from util import naive_postcode_formatter, write_csv
from util.date import round_to_nearest_hour
import pandas as pd
import shutil


working_dir = os.path.join('working')
working_file = os.path.join(working_dir, 'roadshow_attendees.csv')

output_dir = os.path.join('data', 'metrics', 'roadshow_attendees')
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
    data['datetime'] = data['datetime'].apply(round_to_nearest_hour)

    os.makedirs(output_dir, exist_ok=True)

    summary = data.groupby(by='datetime').count()
    pd.DataFrame({
        'attendees': summary.postcode
    }).to_csv(os.path.join(output_dir, 'summary.csv'))

    pc = load_postcodes()

    # Normalise names
    data.postcode = data.postcode.str.upper().str.replace(r'\s+', '', regex=True)
    pc['postcode'] = pc.pcds.str.upper().str.replace(r'\s+', '', regex=True)

    counts = data.postcode.value_counts().to_frame(name='value')
    counts = counts.merge(pc, left_index=True, right_on='postcode')
    pd.DataFrame({
        'postcode': counts.pcds,
        'attendees': counts.value
    }).to_csv(os.path.join(output_dir, 'count_by_postcode.csv'), index=False)

    wards = load_wards_2021()
    by_ward = counts.groupby('osward').value.sum().to_frame().merge(
        wards, left_index=True, right_on='WD21CD', how='left')
    pd.DataFrame({
        'ward_name': by_ward.WD21NM,
        'ward_code': by_ward.WD21CD,
        'attendees': by_ward.value,
    }).to_csv(os.path.join(output_dir, 'count_by_ward.csv'), index=False)

    cons = load_constituencies_2020()
    by_pcon = counts.groupby('pcon').value.sum().to_frame().merge(
        cons, left_index=True, right_on='PCON20CD', how='left')
    pd.DataFrame({
        'constituency_name': by_pcon.PCON20NM,
        'constituency_code': by_pcon.PCON20CD,
        'attendees': by_pcon.value,
    }).to_csv(os.path.join(output_dir, 'count_by_constituency.csv'), index=False)


def process_workshop_attendees(freq='D'):
    data = pd.read_csv(os.path.join(output_dir, 'summary.csv'),
                       parse_dates=['datetime'])
    # Summarises by required frequency and fills in gaps
    data = data.resample('W-Fri', on='datetime').sum().reset_index()

    data.rename(columns={
        'datetime': 'week_ending'
    }, inplace=True)

    data = pd.concat([
        data,
        pd.DataFrame.from_records([{
            'week_ending': data.week_ending.min() - pd.Timedelta(weeks=1),
            'attendees': 0
        }])
    ]).sort_values('week_ending')

    data['cumulative_attendees'] = data.attendees.cumsum()

    data.to_csv(os.path.join(site_dir, 'summary.csv'),
                date_format="%Y-%m-%d", index=False)

    shutil.copy(os.path.join(output_dir, 'count_by_ward.csv'),
                os.path.join(site_dir, 'by_ward.csv'))


if __name__ == '__main__':
    get_workshop_responses()
