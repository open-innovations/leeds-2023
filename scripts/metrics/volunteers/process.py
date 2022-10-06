import logging
import os

from metrics.volunteers.data import load_new_data, load_raw_data, save_raw_data
from metrics.volunteers.setup import VIEW_DIR
from metrics.volunteers.states import update_states
from metrics.volunteers.summarise import summarise_by_ward, summarise_by_week


def update():
    logging.info('Loading data')
    data = load_raw_data()
    new_data = load_new_data()

    logging.info('Combining data')
    data = data.combine_first(new_data)

    logging.info('Updating data')
    data = update_states(data)

    save_raw_data(data)


def summarise():
    data = load_raw_data()
    summarise_by_ward(data, os.path.join(VIEW_DIR, 'by_ward.csv'))
    summarise_by_week(data, os.path.join(VIEW_DIR, 'by_week.csv'))


def patch():
    save_raw_data(load_raw_data())
