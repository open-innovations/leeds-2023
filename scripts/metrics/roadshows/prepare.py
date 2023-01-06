import os
import pandas as pd

from transform import CONTACT_CONSENT_NUMBERS, ROADSHOW_ATTENDANCE_NUMBERS, SUMMARY

VIEW_DIR = os.path.join('docs', 'metrics', 'roadshow-attendees', '_data')
COUNT_BY_DATE = os.path.join(VIEW_DIR, 'by_date.csv')
COUNT_BY_WARD = os.path.join(VIEW_DIR, 'by_ward.csv')

os.makedirs(VIEW_DIR, exist_ok=True)


def load_wards_2021():
    return pd.read_csv(os.path.join('data', 'reference', 'Wards_(December_2021)_GB_BFC.csv'))


def by_ward():
    by_ward = pd.DataFrame({
        'attendance': pd.read_csv(ROADSHOW_ATTENDANCE_NUMBERS).groupby('wd21cd').attendance.sum(),
        'contact_consents': pd.read_csv(CONTACT_CONSENT_NUMBERS).groupby('ward_code').datetime.count(),
    }).reset_index().rename(columns={
        'index': 'ward_code'
    }).fillna(0)

    by_ward.attendance = by_ward.attendance.astype(int)
    by_ward.contact_consents = by_ward.contact_consents.astype(int)

    wards = load_wards_2021()

    by_ward = pd.merge(
        left=by_ward,
        right=wards,
        left_on='ward_code',
        right_on='WD21CD',
    ).rename(columns={
        'WD21NM': 'ward_name'
    })

    by_ward[[
        'ward_name',
        'ward_code',
        'attendance',
        'contact_consents',
    ]].to_csv(COUNT_BY_WARD, index=False)


def by_date():
    summary = pd.read_csv(SUMMARY, parse_dates=['date'])
    summary = summary.resample('W-Fri', on='date').sum().reset_index()
    summary.rename(columns={
        'date': 'week_ending',
        'communication_signup': 'contact_consents'
    }, inplace=True)

    summary = pd.concat([
        summary,
        pd.DataFrame.from_records([{
            'week_ending': summary.week_ending.min() - pd.Timedelta(weeks=1),
            'attendance': 0,
            'contact_consents': 0
        }])
    ]).sort_values('week_ending')
    summary['cumulative_attendance'] = summary.attendance.cumsum()
    summary['cumulative_contact_consents'] = summary.contact_consents.cumsum()

    summary.to_csv(COUNT_BY_DATE,
                   date_format="%Y-%m-%d", index=False)


def prepare():
    by_ward()
    by_date()


if __name__ == '__main__':
    prepare()
