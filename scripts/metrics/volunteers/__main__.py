from datetime import datetime
import logging
import os
from telnetlib import STATUS
import pandas as pd

from data import load_new_data, STATUS_PRE_APPLY, STATUS_APPLY, STATUS_OFFER, STATUS_CONFIRMED, STATUS_DROP

logging.basicConfig(
    format='%(asctime)s|%(levelname)s|%(message)s',
    encoding='utf-8',
    level=logging.DEBUG
)

logging.info('Processing volunteers...')

DATA_DIR = os.path.join('data', 'metrics', 'volunteers')
VIEW_DIR = os.path.join('docs', '_data', 'metrics', 'volunteers')

logging.info('Setting up directories')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VIEW_DIR, exist_ok=True)

logging.info('Loading data')
data = load_new_data()

logging.info('Processing %d entries', len(data))

# Append columns to hold states
states = pd.DataFrame(columns=[
    STATUS_PRE_APPLY,
    STATUS_APPLY,
    STATUS_OFFER,
    STATUS_CONFIRMED,
    STATUS_DROP,
], dtype='datetime64[ns]')
data = pd.concat([data, states])

# Set created date to sign up date
data.loc[data[STATUS_PRE_APPLY].isnull(
), STATUS_PRE_APPLY] = data.sign_up_date.dt.date.astype('datetime64[ns]')

# Set applied date to today's date if applied date is null and the status is one of APPLY. OFFER or CONFIRMED
# NB initial load assumed that the modified date is the time of the status change - as at 5th October
data.loc[
    (data[STATUS_APPLY].isnull()) &
    (data.status.isin([STATUS_APPLY, STATUS_OFFER, STATUS_CONFIRMED, STATUS_DROP])), STATUS_APPLY] = data.modified.dt.date

data.loc[
    (data[STATUS_OFFER].isnull()) &
    (data.status.isin([STATUS_OFFER, STATUS_CONFIRMED])), STATUS_OFFER] = datetime.now().date()

data.loc[
    (data[STATUS_CONFIRMED].isnull()) &
    (data.status.isin([STATUS_CONFIRMED])), STATUS_CONFIRMED] = datetime.now().date()

data.loc[
    (data[STATUS_DROP].isnull()) &
    (data.status.isin([STATUS_DROP])), STATUS_DROP] = datetime.now().date()

data.drop(columns=['sign_up_date', 'modified'], inplace=True)

raw_data = os.path.join(DATA_DIR, 'volunteers.csv')
logging.info('Writing `%s`', raw_data)
data.to_csv(raw_data, index=False)

logging.info('Summarising by ward')
by_ward = data.groupby(['ward_code'])
by_ward = pd.DataFrame({
    STATUS_PRE_APPLY: by_ward[STATUS_PRE_APPLY].count(),
    STATUS_APPLY: by_ward[STATUS_APPLY].count(),
    STATUS_OFFER: by_ward[STATUS_OFFER].count(),
    STATUS_CONFIRMED: by_ward[STATUS_CONFIRMED].count(),
    STATUS_DROP: by_ward[STATUS_DROP].count(),
}).fillna(0).astype(int)

ward_data_file = os.path.join(VIEW_DIR, 'by_ward.csv')
logging.info('Writing `%s`', ward_data_file)
by_ward.to_csv(ward_data_file, na_rep=0)

logging.info('Summarising by week')
by_date = pd.DataFrame({
    STATUS_PRE_APPLY: data.groupby(STATUS_PRE_APPLY).hash.count(),
    STATUS_APPLY: data.groupby(STATUS_APPLY).hash.count(),
    STATUS_OFFER: data.groupby(STATUS_OFFER).hash.count(),
    STATUS_CONFIRMED: data.groupby(STATUS_CONFIRMED).hash.count(),
    STATUS_DROP: data.groupby(STATUS_DROP).hash.count(),
})
by_date.index = by_date.index.astype('datetime64[ns]')
by_date.index.names = ['week_ending']
by_date = by_date.resample('W-Fri').sum().fillna(0).astype(int)

weekly_data_file = os.path.join(VIEW_DIR, 'by_week.csv')
logging.info('Writing `%s`', weekly_data_file)
by_date.cumsum().to_csv(weekly_data_file, na_rep=0)

logging.info('Done!')
# pd.DataFrame({
#     'total': by_ward.hash.count(),
#     STATUS_APPLY: data[data.status == STATUS_APPLY].groupby('ward_code').hash.count(),
#     STATUS_OFFER: data[data.status == STATUS_OFFER].groupby('ward_code').hash.count(),
#     STATUS_CONFIRMED: data[data.status == STATUS_CONFIRMED].groupby('ward_code').hash.count(),
# }).to_csv(os.path.join(VIEW_DIR, 'ward.csv'), na_rep=0)
