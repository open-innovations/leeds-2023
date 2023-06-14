import os
import pandas as pd

from lib.util.convert import literal_converter
from scripts.util.geography import normalise_leeds_wards, ward_name_to_code


def data_path(event):
    data_dir = os.path.join('docs', 'metrics', 'events', event, '_data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def project_data(data, name, type='Produce (Signature)'):

    filtered = data.loc[(data.project_name == name) &
                        (data.project_type == type)]
    return filtered


def summarise_events(events):
    result = pd.DataFrame({
        'events': events.groupby('start_date').event_name.count(),
        'attendances_in_person': events.groupby('start_date').actual_audience_size_number_of_participants_in_person.sum(),
        'attendances_online': events.groupby('start_date').actual_audience_size_number_of_participants_online.sum(),
    }).resample('W-FRI').sum().astype(int)
    result['cumulative_events'] = result.events.cumsum()
    result['cumulative_attendances_in_person'] = result.attendances_in_person.cumsum()
    result['cumulative_attendances_online'] = result.attendances_online.cumsum()

    return result


def prepare_project(events, name, key):
    data_dir = data_path(key)

    filtered = events.pipe(project_data, name=name)

    project_events = filtered.pipe(summarise_events)
    project_events.to_csv(os.path.join(data_dir, 'by_date.csv'))

    headlines = project_events.drop(
        columns=project_events.columns[~project_events.columns.str.match('cumulative_')]
    ).rename(
        columns=lambda c: c.replace('cumulative_', '')
    ).iloc[-1]
    headlines['latest_date'] = headlines.name
    headlines.to_json(os.path.join(data_dir, 'headlines.json'), orient='table', date_format='iso')

    ward_counts = filtered['ward_(from_venue)'].pipe(literal_converter).explode().value_counts()
    ward_counts.name = 'count'
    ward_counts.index.name = 'ward'
    ward_counts = ward_counts.reset_index()
    ward_counts['ward_name'] = ward_counts.ward.pipe(normalise_leeds_wards)
    ward_counts.drop(columns=['ward'], inplace=True)
    ward_counts['ward_code'] = ward_counts.ward_name.pipe(ward_name_to_code)
    ward_counts.to_csv(os.path.join(data_dir, 'by_ward.csv'), index=False)


if __name__ == '__main__':
    from transform import ALL_EVENTS
    events = pd.read_csv(ALL_EVENTS, parse_dates=['start_date', 'end_date'])

    events.pipe(prepare_project, name='05 - The Barn', key='the_barn')
