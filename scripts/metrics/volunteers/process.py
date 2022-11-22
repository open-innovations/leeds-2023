import logging
import os

from metrics.volunteers.data import load_new_data, load_raw_data, save_raw_data
from metrics.volunteers.setup import VIEW_DIR
from metrics.volunteers.states import update_states
from metrics.volunteers.summarise import summarise_by_ward, summarise_by_week,summarise_by_local_authority

import util.oi_sftp_server


def update():
    logging.info('Getting latest data')
    logging.debug(os.getcwd())
    util.oi_sftp_server.get('rosterfy/current-checkpoint.csv', 'working/rosterfy/current-checkpoint.csv')

    logging.info('Loading data')
    data = load_raw_data()
    new_data = load_new_data()

    logging.info('Combining data')
    # Capture some stats
    old_rowcount = data.shape[0]
    new_rowcount = new_data.shape[0]
    # Copy the statust to a new column
    new_data['new_status'] = new_data.status
    # Merge the datasets! data wins!
    data = data.combine_first(new_data)
    # Count how many rows have changed (i.e. were in the old dataset and have new status)
    changed_rowcount = data[data.status != data.new_status].shape[0]
    # Overwrite the status column
    data.status = data.new_status
    # Remove the new_status column
    data.drop(columns=['new_status'], inplace=True)
    logging.info('Adding {new} and updating status for {changes} volunteers'.format(
      new=new_rowcount - old_rowcount,
      changes=changed_rowcount
    ))

    logging.info('Updating dates for the states')
    data = update_states(data)

    save_raw_data(data)


def summarise():
    data = load_raw_data()
    summarise_by_ward(data, os.path.join(VIEW_DIR, 'by_ward.csv'))
    summarise_by_week(data, os.path.join(VIEW_DIR, 'by_week.csv'))
    summarise_by_local_authority(data, os.path.join(VIEW_DIR, 'by_local_authority.csv'),os.path.join(VIEW_DIR, 'la_stats.json'))


def patch():
    save_raw_data(load_raw_data())
