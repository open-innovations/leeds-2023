import os
import pandas as pd

from transform import SCHOOLS_DATA, literal_converter

SITE_DATA = os.path.join('docs', 'metrics', 'schools', '_data')
os.makedirs(SITE_DATA, exist_ok=True)


SCHOOLS_REF_DATA = os.path.join('data', 'reference', 'schools.csv')
WARD_REFERENCE = os.path.join('data', 'reference', 'leeds_wards.csv')

all_schools = pd.read_csv(SCHOOLS_REF_DATA, usecols = ['school_name', 'ward'])
leeds_wards = pd.read_csv(WARD_REFERENCE)


def load_schools_data():
    return pd.read_csv(SCHOOLS_DATA, parse_dates=['date']).apply(literal_converter)


if __name__ == "__main__":

    data = load_schools_data()

    summary = {}

    summary['schools_in_leeds'] = len(all_schools)

    # Pupils engaged over time
    pupil_engagements = data.groupby(
        'date').participant_count.sum().resample('W-FRI').sum().astype(int)
    school_engagements = data.groupby(
        'date').school_count.sum().resample('W-FRI').sum()
    cumulative_pupil_engagements = pupil_engagements.cumsum()
    cumulative_school_engagements = school_engagements.cumsum()

    engagements_by_week = pd.DataFrame({
        'pupil_engagements': pupil_engagements,
        'cumulative_pupil_engagements': cumulative_pupil_engagements,
        'school_engagements': school_engagements,
        'cumulative_school_engagements': cumulative_school_engagements,
    })

    engagements_by_week.to_csv(os.path.join(
        SITE_DATA, 'engagements_by_week.csv'))
    summary['total_pupil_engagements'] = engagements_by_week.pupil_engagements.sum()
    summary['total_school_engagements'] = engagements_by_week.school_engagements.sum()

    schools_counts = data.set_index(
        'date').schools.explode().dropna().value_counts()
    schools_counts.index.rename('school', inplace=True)
    schools_counts.rename('count_of_engagements', inplace=True)
    schools_counts.to_csv(os.path.join(
        SITE_DATA, 'school_engagement_counts.csv'))

    summary['unique_schools'] = schools_counts.count()
    summary['percentage_of_leeds_schools_engaged'] = (summary['unique_schools'] / summary['schools_in_leeds'] * 100).round(1)

    summary['date_built'] = pd.Timestamp.today().floor('D').strftime('%Y-%m-%d')
    summary['earliest_date'] = data.date.min().strftime('%Y-%m-%d')

    engagements_all_schools = all_schools.merge(
        how='outer',
        right=schools_counts,
        left_on= 'school_name', 
        right_on='school',
        validate='many_to_many',
    )
    engagements_by_ward = leeds_wards.merge(
        how='outer',
        right=engagements_all_schools,
        left_on= 'WD21NM',
        right_on='ward',
        validate='one_to_many',
    )
    pd.DataFrame({
        'count': engagements_by_ward.groupby(['WD21CD', 'WD21NM']).count_of_engagements.sum().fillna(0).astype(int)
    }).to_csv(
        os.path.join(SITE_DATA, 'engagements_by_ward.csv')
    )

    # Construct summary dataframe and output to JSON
    summary = pd.DataFrame.from_dict(
        summary, orient="index", columns=['value'])
    summary.value.to_json(os.path.join(SITE_DATA, 'headlines.json'))
