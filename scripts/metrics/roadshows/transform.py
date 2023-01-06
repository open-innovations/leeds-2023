import os
import pandas as pd
from thefuzz import process
from util.geography import match_ward

from extract import WORKING_DIR, CONTACT_CONSENT_RESPONSES


OUTPUT_DIR = os.path.join('data', 'metrics', 'roadshows')
ROADSHOW_ATTENDANCE_NUMBERS = os.path.join(OUTPUT_DIR, 'attendance.csv')
CONTACT_CONSENT_NUMBERS = os.path.join(OUTPUT_DIR, 'contact_consents.csv')
SUMMARY = os.path.join(
    OUTPUT_DIR, 'attendance_and_communication_signup_summary.csv')

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_wards_2021():
    return pd.read_csv(os.path.join('data', 'reference', 'Wards_(December_2021)_GB_BFC.csv'))


def process_attendance_spreadsheet():
    wards = load_wards_2021()
    # Remove more southerly wards
    wards = wards.drop(wards[wards['LAT'] < 52].index)
    wards = pd.DataFrame({
        'wd21cd': wards.WD21CD,
        'wd21nm': wards.WD21NM
    })

    data = pd.read_excel(os.path.join(WORKING_DIR,
                                      'Leeds 2023 Roadshow Open Innovations.xlsx'), sheet_name='Sheet1')
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


def process_contract_consents():
    contact_consents = pd.read_csv(CONTACT_CONSENT_RESPONSES, parse_dates=['datetime'])
    contact_consents['datetime'] = contact_consents['datetime'].dt.tz_localize(None).dt.round(freq='H')
    contact_consents = match_ward(contact_consents, postcode_field='postcode')

    contact_consents[['datetime', 'ward_code']].sort_values(by=['datetime', 'ward_code']).to_csv(
        CONTACT_CONSENT_NUMBERS, index=False)


def create_summary():
    attendance = pd.read_csv(ROADSHOW_ATTENDANCE_NUMBERS, parse_dates=['date'])
    # attendance.rename(columns={'date': 'datetime'}, inplace=True)

    contact_consents = pd.read_csv(CONTACT_CONSENT_NUMBERS, parse_dates=['datetime'])
    contact_consents['date'] = contact_consents.datetime.dt.round(freq='D')

    attendance_summary = attendance.groupby(
        by='date').sum(numeric_only=True)

    contact_consents_summary = contact_consents.groupby(by='date').count()
    contact_consents_summary = pd.DataFrame({
        'communication_signup': contact_consents_summary.ward_code
    })

    summary = pd.concat([attendance_summary, contact_consents_summary]).groupby(
        'date').sum().astype(int)
    summary.to_csv(SUMMARY, date_format='%Y-%m-%d')


if __name__ == "__main__":
    process_attendance_spreadsheet()
    process_contract_consents()
    create_summary()
