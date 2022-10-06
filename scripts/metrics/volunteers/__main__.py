from datetime import datetime
import logging
import os
from telnetlib import STATUS
import pandas as pd

from data import load_new_data, save_raw_data, DATA_DIR, VIEW_DIR
from states import add_states, STATUS_PRE_APPLY, STATUS_APPLY, STATUS_OFFER, STATUS_CONFIRMED, STATUS_DROP
from summarise import summarise_by_ward, summarise_by_week


logging.basicConfig(
    format='%(asctime)s|%(levelname)s|%(message)s',
    encoding='utf-8',
    level=logging.DEBUG
)

logging.info('Processing volunteers...')

logging.info('Setting up directories')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VIEW_DIR, exist_ok=True)

logging.info('Loading data')
data = load_new_data()

logging.info('Processing %d entries', len(data))
data = add_states(data)

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

save_raw_data(data)

summarise_by_ward(data, os.path.join(VIEW_DIR, 'by_ward.csv'))
summarise_by_week(data, os.path.join(VIEW_DIR, 'by_week.csv'))

logging.info('Done!')
