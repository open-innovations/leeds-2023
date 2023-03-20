import logging
import os
from glob import glob
from hashlib import blake2s

import pandas as pd
from metrics.volunteers.setup import WORKING_DIR, DATA_DIR
from metrics.volunteers.states import (STATUS_APPLY, STATUS_CONFIRMED,
                                       STATUS_DROP, STATUS_OFFER,
                                       STATUS_PRE_APPLY, add_states,
                                       map_checkpoints_to_states)
from util.geography import match_la, match_ward

file_path = os.path.join(DATA_DIR, 'volunteers.csv')
RAW_DATA = os.path.join(WORKING_DIR, 'current-checkpoint.csv')


def hash_id(id):
    the_hash = blake2s(digest_size=10)
    # Could do with salting this hash
    the_hash.update(bytes(str(id), 'utf-8'))
    return the_hash.hexdigest()


def load_source_data_file(path):
    data = pd.read_csv(path)
    data = data.rename(columns={
        'User - ID': 'id',
        'User - Sign Up Date': 'sign_up_date',
        'User - Postal Code': 'postcode',
        'User - Checkpoint': 'checkpoint',
        'User - Modified Date': 'modified',
    })

    # We want to map postcodes to ward codes
    data = match_ward(data, postcode_field='postcode', ward_column='ward_code')
    data = match_la(data, postcode_field='postcode', la_column='local_authority_code')

    # Report the entries which don't map to wards
    no_ward = data[data.ward_code == 'UNKNOWN']
    no_ward = pd.DataFrame({
        'id': no_ward.id,
        'postcode': no_ward.postcode,
        'checkpoint': no_ward.checkpoint,
    })
    no_ward.to_csv('working/rosterfy_errors.csv', index=False)

    # We need to use the id between runs to identify state
    # change dates. We don't want to keep the proper hash
    data['hash'] = data.id.apply(hash_id)

    # Make sure dates are valid
    data.sign_up_date = pd.to_datetime(data.sign_up_date)
    data.modified = pd.to_datetime(data.modified)

    # Map checkpoint to status
    data['status'] = map_checkpoints_to_states(data.checkpoint)

    # Add empty placeholders for states
    data = add_states(data)

    # Remove potentially personal data
    data = data.drop(columns=['id', 'postcode', 'checkpoint'])

    # Set the hash to the index
    data = data.set_index('hash')

    return data


def load_new_data():
    data = load_source_data_file(RAW_DATA)
    return data


def load_raw_data():
    return pd.read_csv(file_path,
                       index_col=['hash'],
                       parse_dates=[
                           STATUS_PRE_APPLY,
                           STATUS_APPLY,
                           STATUS_OFFER,
                           STATUS_CONFIRMED,
                           STATUS_DROP
                       ])


def save_raw_data(data):
    logging.info('Writing `%s`', file_path)
    data.sort_values(by=['created', 'hash'], ascending=[True, True])[
        [
          'ward_code', 'local_authority_code', 'status', 'current', 'created', 'applied', 'offered', 'confirmed', 'rejected'
        ]
    ].to_csv(file_path)
