import os
import sys
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.realpath(os.path.join(
    os.path.dirname(__file__), '../../../../'))
lib_dir = os.path.abspath(os.path.join(PROJECT_ROOT, 'lib/'))
if not lib_dir in sys.path:
    sys.path.append(lib_dir)

import util.geo
import util.convert


def load_event_data():
    all_data_file = os.path.join(
        PROJECT_ROOT,
        'data/metrics/events/master/all.csv'
    )
    data = (
        pd.read_csv(all_data_file, parse_dates=['start_date'])
          .pipe(filter_signature_events)
    )
    return data


def filter_signature_events(data):
    return data.loc[
        (data.project_type == 'Produce (Signature)') &
        (data.event_type.str.contains('Public Event -'))
    ]
    # (data.project_name == '12 - My LEEDS 2023') &
    # (data.start_date < pd.Timestamp.now())


def filter_by_project(data, project_name):
    return data.loc[
        data.project_name == project_name
    ]


def prepare(data):
    return data.pipe(add_wards).pipe(calculate_audience_size)


def save_files(data, OUT_DIR):
    return data.pipe(
        save_stats_by_ward, OUT_DIR
    ).pipe(
        save_stats_by_week, OUT_DIR
    ).pipe(
        save_stats_by_month, OUT_DIR
    ).pipe(
        save_headlines, OUT_DIR
    )


def get_wards(data):
    return data['ward_(from_venue)'].fillna(value='[]').pipe(util.convert.literal_converter).apply(np.unique)


def count_wards(data):
    return data.pipe(get_wards).apply(len)


def get_first_ward(data):
    return data.pipe(get_wards).apply(lambda x: x[0] if len(x) > 0 else np.nan)


def normalise_ward(series):
    name = series.pipe(util.geo.normalise_leeds_wards)
    code = name.pipe(util.geo.ward_name_to_code)
    return pd.DataFrame({
        'ward_name': name,
        'ward_code': code
    }, index=series.index)


def add_wards(data):
    return pd.concat([
        data,
        data.pipe(get_first_ward).pipe(normalise_ward)
    ], axis=1)


def calculate_audience_size(data):
    data['audience_size'] = data.actual_audience_size_number_of_participants_in_person.fillna(
        0) + data.actual_audience_size_number_of_participants_online.fillna(0)
    return data


def by_ward(data):
    return pd.DataFrame(
        {
            'events': data.groupby('ward_code').audience_size.count(),
            'audience': data.groupby('ward_code').audience_size.sum(),
        }
    )


def by_month(data):
    by_month = pd.DataFrame({
        'events': data.groupby('start_date').audience_size.count(),
        'audience': data.groupby('start_date').audience_size.sum().astype(int)
    }).resample('M').sum()
    by_month.index.name = 'month_ending'
    by_month['cumulative_events'] = by_month.events.cumsum()
    by_month['cumulative_audience'] = by_month.audience.cumsum()
    return by_month


def save_stats_by_ward(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    data.pipe(by_ward).to_csv(os.path.join(output_dir, 'by_ward.csv'))
    return data


def save_stats_by_week(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    by_week = pd.DataFrame({
        'events': data.groupby('start_date').audience_size.count(),
        'audience': data.groupby('start_date').audience_size.sum().astype(int)
    }).resample('W-FRI').sum()
    by_week.index.name = 'week_ending'
    by_week['cumulative_events'] = by_week.events.cumsum()
    by_week['cumulative_audience'] = by_week.audience.cumsum()

    by_week.to_csv(os.path.join(output_dir, 'by_week.csv'))
    return data


def save_stats_by_month(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    data.pipe(by_month).to_csv(os.path.join(output_dir, 'by_month.csv'))
    return data


def save_headlines(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    headlines = data.pipe(by_month).drop(
        columns=['events', 'audience']
    ).rename(
        columns=lambda n: n.replace('cumulative', 'total')
    ).iloc[-1]
    headlines['ward_count'] = len(data.pipe(by_ward).index)
    headlines['earliest_date'] = data.start_date.min()
    headlines['latest_date'] = data.start_date.max()
    headlines.to_json(os.path.join(output_dir, 'headlines.json'), indent=2, date_format='iso')
    return data


