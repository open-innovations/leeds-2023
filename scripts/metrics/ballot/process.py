import os
import logging

import pandas as pd
from util.firebase import pull_collection
from util.geography import match_ward, match_la

DATA_DIR = os.path.join('data', 'metrics', 'ballot')
RAW_DATA = os.path.join(DATA_DIR, 'ballot_entries.csv')


def get_data():
    logging.info("Querying ballot database")
    data = pull_collection(
      collection_name=u'ballot-entries',
      fields=[
        'dateSubmitted',
        'hasPostcode',
        'postcode',
        'artistAgeGroup',
        'artworkMedium',
        'source',
    ])
    logging.info("Got %d entries", data.shape[0])

    # Map postcode to ward
    logging.info("Mapping wards")
    data = match_ward(data)
    data.loc[data.hasPostcode == False, 'ward_code'] = 'NOT_PROVIDED'

    # Map postcode to local authority
    logging.info("Mapping local authorities")
    data = match_la(data)
    data.loc[data.hasPostcode == False, 'la_code'] = 'NOT_PROVIDED'

    # Remove postcode and hasPostcode columns
    data = data.drop(columns=['postcode', 'hasPostcode'])

    # Rename columns
    data = data.rename(columns={
        'dateSubmitted': 'date_submitted',
        'artistAgeGroup': 'artist_age_group',
        'artworkMedium': 'artwork_medium',
    })

    # Convert and round the date
    data.date_submitted = pd.DatetimeIndex(
        data.date_submitted).tz_localize(None).floor('D')

    return data


def save_raw_data(data):
    cols = [
      'date_submitted',
      'la_code',
      'ward_code',
      'artist_age_group',
      'artwork_medium',
      'source',
    ]
    os.makedirs(DATA_DIR, exist_ok=True)
    logging.info("Saving %s", RAW_DATA)
    data[cols].sort_values(
        by=cols,
        ignore_index=True
    ).to_csv(
        RAW_DATA, index=False
    )


def load_raw_data():
    logging.info("Loading %s", RAW_DATA)
    data = pd.read_csv(RAW_DATA, parse_dates=['date_submitted'])
    return data


def update():
    logging.info('Updating ballot data')
    data = get_data()
    save_raw_data(data)
    logging.info('Completed ballot data update')

if __name__ == '__main__':
    update()
