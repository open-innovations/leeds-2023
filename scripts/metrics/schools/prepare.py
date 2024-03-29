import os
import pandas as pd

from scripts.util.geography import fuzzy_match_leeds_wards
from scripts.util.logger import logging, log_formatter
from config import SCHOOLS_DATA, literal_converter

logger = logging.getLogger('schools.prepare')
log_handler = logging.FileHandler('working/log/schools_prepare.log', mode='w', encoding='utf-8')
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.info('Set up logging')

SITE_DATA = os.path.join('docs', 'metrics', 'schools', '_data')
os.makedirs(SITE_DATA, exist_ok=True)

UNIQUE_SCHOOLS_OVERRIDE = 228


SCHOOLS_REF_DATA = os.path.join('data', 'reference', 'schools.csv')
WARD_REFERENCE = os.path.join('data', 'reference', 'leeds_wards.csv')

all_schools = pd.read_csv(SCHOOLS_REF_DATA, usecols=[
                          'school_name', 'ward', 'ward_code'])
leeds_wards = pd.read_csv(WARD_REFERENCE)


def load_schools_data():
    return pd.read_csv(SCHOOLS_DATA, parse_dates=['date']).apply(literal_converter)


if __name__ == "__main__":

    data = load_schools_data()

    summary = {}

    summary['schools_in_leeds'] = len(all_schools)
    summary['schools_not_assigned_to_ward'] = len(
        all_schools[all_schools.ward.isna()])

    # Pupils engaged over time
    pupil_engagements = data.groupby(
        'date').pupil_count.sum().resample('W-FRI').sum().astype(int)
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

    schools_counts = data.schools.explode().value_counts().to_frame()
    schools_counts.index.rename('school', inplace=True)
    schools_counts.columns = ['count_of_engagements']
    schools_counts = schools_counts.merge(
        right=all_schools.set_index('school_name'),
        left_index=True,
        right_index=True,
    )
    schools_counts.index.names = ['school']
    schools_counts.to_csv(os.path.join(
        SITE_DATA, 'school_engagement_counts.csv'))

    summary['unique_schools'] = int(UNIQUE_SCHOOLS_OVERRIDE)
    summary['percentage_of_leeds_schools_engaged'] = (
        summary['unique_schools'] / summary['schools_in_leeds'] * 100)

    summary['date_built'] = pd.Timestamp.today().floor(
        'D').strftime('%Y-%m-%d')
    summary['earliest_date'] = data.date.min().strftime('%Y-%m-%d')

    summary['engagements_with_schools_not_assigned_to_ward'] = schools_counts[schools_counts.ward.isna(
    )].count_of_engagements.sum().astype(int)

    ward_stats = leeds_wards.merge(
        schools_counts.reset_index(),
        how='left',
        left_on='WD21CD',
        right_on='ward_code',
    )

    pupils_per_ward = data[['pupil_count', 'wards']].explode('wards').rename(
        columns={
            'wards': 'ward_name',
        }
    )
    try:
      assert len(pupils_per_ward.index) == len(data.index), 'Multiple schools per line in source data when exploding for pupil counts'
    except Exception as e:
      logger.error(e)

    pupils_per_ward = fuzzy_match_leeds_wards(pupils_per_ward, ward_name_col='ward_name')

    ward_group = ward_stats.groupby(['WD21CD', 'WD21NM'])
    engagements_by_ward = pd.DataFrame({
        'schools_engaged': ward_group.count_of_engagements.count(),
        'total_engagements': ward_group.count_of_engagements.sum(),
        'count_of_schools': all_schools.groupby(['ward_code', 'ward']).school_name.count(),
        'pupil_engagements': pupils_per_ward.groupby(['ward_code', 'ward_name']).pupil_count.sum(),
    }).fillna(0).astype(int)
    try:
      assert engagements_by_ward.pupil_engagements.sum() == data[data.wards.notna()].pupil_count.sum()
    except Exception as e:
      logger.error(e)

    summary['engagements_with_pupils_not_assigned_to_ward'] = (data.pupil_count.sum() - engagements_by_ward.pupil_engagements.sum()).astype(int)

    engagements_by_ward.index.names = ['ward_code', 'ward']
    engagements_by_ward['percent_of_schools_in_ward_engaged'] = (engagements_by_ward.schools_engaged / engagements_by_ward.count_of_schools * 100).round(1)

    engagements_by_ward \
        .to_csv(os.path.join(SITE_DATA, 'engagements_by_ward.csv'))

    # Construct summary dataframe and output to JSON
    summary = pd.DataFrame.from_dict(
        summary, orient="index", columns=['value']).sort_index()
    summary.value.to_json(os.path.join(SITE_DATA, 'headlines.json'), indent=2)
