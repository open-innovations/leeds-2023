import logging
import os

logging.basicConfig(
    format='%(asctime)s|%(levelname)s|%(message)s',
    encoding='utf-8',
    level=logging.DEBUG
)

from metrics.volunteers.data import load_new_data, save_raw_data
from metrics.volunteers.setup import VIEW_DIR
from metrics.volunteers.states import (STATUS_APPLY, override_state_date,
                                       set_applied_date, set_confirmed_date,
                                       set_created_date, set_dropped_date,
                                       set_offer_date)
from metrics.volunteers.summarise import summarise_by_ward, summarise_by_week

logging.info('Processing volunteers...')

logging.info('Loading data')
data = load_new_data()

logging.info('Processing %d entries', len(data))

data = set_created_date(data)
# data = set_applied_date(data)
data = override_state_date(data, STATUS_APPLY)
data = set_offer_date(data)
data = set_confirmed_date(data)
data = set_dropped_date(data)

data.drop(columns=['sign_up_date', 'modified'], inplace=True)

save_raw_data(data)

summarise_by_ward(data, os.path.join(VIEW_DIR, 'by_ward.csv'))
summarise_by_week(data, os.path.join(VIEW_DIR, 'by_week.csv'))

logging.info('Done!')
