import logging
import os

import pandas as pd
from metrics.ballot.process import load_raw_data
from util.geography import local_authority_stats

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
    by_la = pd.DataFrame({
        'submissions': data.groupby('la_code').date_submitted.count()
    })
    by_la.to_csv(os.path.join(VIEW_DIR, 'by_local_authority.csv'))
    stats = local_authority_stats(codes=by_la.index, counts=by_la.submissions)
    stats.to_json(os.path.join(VIEW_DIR, 'local_autority_stats.json'))


def by_date():
    logging.info('Summarising by date')
    data = load_raw_data()
    data = pd.DataFrame({
        'submissions': data.groupby('date_submitted').ward_code.count(),
    }).resample('D').sum().fillna(0).astype(int)
    data['cumulative_submissions'] = data.submissions.cumsum()
    data.index.set_names(['date_submitted'])

    data.to_csv(os.path.join(VIEW_DIR, 'by_date.csv'))


def by_age():
    logging.info('Summarising by age')
    data = load_raw_data()
    data = pd.DataFrame({
        'submissions': data.groupby('artist_age_group').ward_code.count(),
    }).fillna(0).astype(int)
    data.index.set_names(['artist_age_group'])
    data = data.reindex(index=[
      'under16',
      '16-19',
      '20-24',
      '25-29',
      '30-34',
      '35-39',
      '40-44',
      '45-49',
      '50-54',
      '55-59',
      '60-64',
      '65-69',
      '70-74',
      '75-79',
      'over85',
      'unspecified'
    ])

    data.to_csv(os.path.join(VIEW_DIR, 'by_age.csv'))


def by_source():
    logging.info('Summarising by source')
    data = load_raw_data()
    data = pd.DataFrame({
        'submissions': data.groupby('source').ward_code.count(),
    }).fillna(0).astype(int)
    data.index.set_names(['source'])

    data.to_csv(os.path.join(VIEW_DIR, 'by_source.csv'))


def all():
    by_ward()
    by_local_authority()
    by_date()
    by_age()
    by_source()
