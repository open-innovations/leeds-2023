import os
import pandas as pd

from transform import SCHOOLS_DATA, literal_converter

SITE_DATA = os.path.join('docs', 'metrics', 'schools', '_data')
os.makedirs(SITE_DATA, exist_ok=True)


def load_schools_data():
    return pd.read_csv(SCHOOLS_DATA, parse_dates=['date']).apply(literal_converter)


if __name__ == "__main__":

    data = load_schools_data()

    summary = {}

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

    # Construct summary dataframe and output to JSON
    summary = pd.DataFrame.from_dict(
        summary, orient="index", columns=['value'])
    summary.value.to_json(os.path.join(SITE_DATA, 'summary.json'))
