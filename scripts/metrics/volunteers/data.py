import logging
import os
from glob import glob
from hashlib import blake2s

import pandas as pd

from postcode import match_ward
from states import map_checkpoints_to_states

DATA_DIR = os.path.join('data', 'metrics', 'volunteers')
VIEW_DIR = os.path.join('docs', '_data', 'metrics', 'volunteers')


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

    # Remove potentially personal data
    data = data.drop(columns=['id', 'postcode', 'checkpoint'])

    return data


def load_new_data():
    files = glob('working/rosterfy/*.csv')
    data = pd.concat(
        [load_source_data_file(f) for f in files]
    )

    return data


def save_raw_data(data):
    file_path = os.path.join(DATA_DIR, 'volunteers.csv')
    logging.info('Writing `%s`', file_path)
    data.to_csv(file_path, index=False)
