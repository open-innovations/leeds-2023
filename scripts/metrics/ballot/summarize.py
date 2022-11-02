import logging
import os

import pandas as pd
from metrics.ballot.process import load_raw_data

VIEW_DIR = os.path.join('docs', '_data', 'metrics', 'ballot')
os.makedirs(VIEW_DIR, exist_ok=True)


def by_ward():
    logging.info('Summarising by ward')
    data = load_raw_data()
    pd.DataFrame({
        'submissions': data.groupby('ward_code').date_submitted.count()
    }).to_csv(os.path.join(VIEW_DIR, 'by_ward.csv'))


def by_local_authority():
    logging.info('Summarising by local_authority')
    data = load_raw_data()
    pd.DataFrame({
        'submissions': data.groupby('la_code').date_submitted.count()
    }).to_csv(os.path.join(VIEW_DIR, 'by_local_authority.csv'))


def by_date():
    logging.info('Summarising by date')
    data = load_raw_data()
    data = pd.DataFrame({
        'submissions': data.groupby('date_submitted').ward_code.count(),
    }).resample('D').sum().fillna(0).astype(int)
    data['cumulative_submissions'] = data.submissions.cumsum()
    data.index.set_names(['date_submitted'])

    data.to_csv(os.path.join(VIEW_DIR, 'by_date.csv'))
