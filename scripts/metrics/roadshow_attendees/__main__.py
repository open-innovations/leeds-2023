from __future__ import print_function

import os

import pandas as pd
from thefuzz import process
from typeform import get_field_from_item, get_responses
from util import naive_postcode_formatter, write_csv
from util.date import round_to_nearest_hour

WORKING_DIR = os.path.join('working')
CONTACT_CONSENT_RESPONSES = os.path.join(WORKING_DIR, 'contact_consent_responses.csv')

OUTPUT_DIR = os.path.join('data', 'metrics', 'roadshows')
ROADSHOW_ATTENDANCE_NUMBERS = os.path.join(OUTPUT_DIR, 'attendance.csv')
SUMMARY = os.path.join(OUTPUT_DIR, 'attendance_and_communication_signup_summary.csv')

VIEW_DIR = os.path.join('docs', '_data', 'metrics', 'roadshows')
ROADSHOW_SUMMARY = os.path.join(VIEW_DIR, 'summary.csv')
COUNT_BY_WARD = os.path.join(VIEW_DIR, 'by_ward.csv')


def load_postcodes():
    return pd.read_csv(os.path.join('data', 'reference', 'postcodes.csv'))


def load_wards_2021():
    return pd.read_csv(os.path.join('data', 'reference', 'Wards_(December_2021)_GB_BFC.csv'))


def load_constituencies_2020():
    return pd.read_csv(os.path.join('data', 'reference', 'Westminster_Parliamentary_Constituencies_(December_2020)_UK_BFC.csv'))


def get_contact_consent_responses():
    form_id = 'vm2OxH3L'
    postcode_field_id = 'GHOzEy9LwD8o'
    roadshow_data = get_responses(form_id, fields=postcode_field_id)

    def get_time_and_postcode(item):
        postcode = get_field_from_item(
            item, postcode_field_id)
        return {
            'datetime': item['submitted_at'],
            'postcode': naive_postcode_formatter(postcode)
        }

    data = [get_time_and_postcode(x) for x in roadshow_data['items']]

    write_csv(data, CONTACT_CONSENT_RESPONSES,
              field_names=['datetime', 'postcode'])


def process_attendance_spreadsheet():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
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
      'attendance': data.attendees
    })
    data = data.sort_values(by='date')
    data.to_csv(ROADSHOW_ATTENDANCE_NUMBERS, index=False)


def prepare_roadshow_data():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(VIEW_DIR, exist_ok=True)

    contact_consents = pd.read_csv(CONTACT_CONSENT_RESPONSES)
    contact_consents['datetime'] = pd.to_datetime(contact_consents['datetime']).dt.round(freq='D')

    attendance = pd.read_csv(ROADSHOW_ATTENDANCE_NUMBERS)
    attendance.rename(columns={ 'date': 'datetime' }, inplace=True)
    attendance['datetime'] = pd.to_datetime(attendance['datetime'], utc=True)

    attendance_summary = attendance.groupby(by='datetime').sum()

    contact_consents_summary = contact_consents.groupby(by='datetime').count()
    contact_consents_summary = pd.DataFrame({
        'communication_signup': contact_consents_summary.postcode
    })

    summary = pd.concat([attendance_summary, contact_consents_summary]).groupby('datetime').sum().astype(int)
    summary.index.names=['date']
    summary.to_csv(SUMMARY, date_format='%Y-%m-%d')

    pc = load_postcodes()

    # Normalise names
    contact_consents.postcode = contact_consents.postcode.str.upper().str.replace(r'\s+', '', regex=True)
    pc['postcode'] = pc.pcds.str.upper().str.replace(r'\s+', '', regex=True)

    counts = contact_consents.postcode.value_counts().to_frame(name='contact_consents')
    counts = counts.merge(pc, left_index=True, right_on='postcode')

    responses_by_ward = pd.DataFrame({
      'wd21cd': counts.osward,
      'contact_consents': counts.contact_consents,
    })
    attendees_by_ward = pd.DataFrame({
      'wd21cd': attendance.wd21cd,
      'attendees': attendance.attendance
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
        'attendance': by_ward.attendees.astype(int),
        'contact_consents': by_ward.contact_consents.astype(int),
    }).to_csv(COUNT_BY_WARD, index=False)


def process_roadshow_attendees(freq='D'):
    data = pd.read_csv(SUMMARY,
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
            'attendance': 0,
            'contact_consents': 0
        }])
    ]).sort_values('week_ending')

    data['cumulative_attendance'] = data.attendance.cumsum()
    data['cumulative_contact_consents'] = data.contact_consents.cumsum()

    data.to_csv(ROADSHOW_SUMMARY,
                date_format="%Y-%m-%d", index=False)

get_contact_consent_responses()
# process_attendance_spreadsheet()
prepare_roadshow_data()
