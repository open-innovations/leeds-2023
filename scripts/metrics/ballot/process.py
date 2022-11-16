import sys
import os
import logging

import pandas as pd
from util.firebase import pull_collection
from util.geography import match_ward, match_la

DATA_DIR = os.path.join('data', 'metrics', 'ballot')
RAW_DATA = os.path.join(DATA_DIR, 'ballot_entries.csv')
RAW_GROUP_DATA = os.path.join(DATA_DIR, 'ballot_group_entries.csv')


def geo_match(data, hasPostcodeField='hasPostcode'):
    # Map postcode to ward
    logging.info("Mapping wards")
    data = match_ward(data)
    data.loc[data[hasPostcodeField] == False, 'ward_code'] = 'NOT_PROVIDED'

    # Map postcode to local authority
    logging.info("Mapping local authorities")
    data = match_la(data)
    data.loc[data[hasPostcodeField] == False, 'la_code'] = 'NOT_PROVIDED'

    # Remove postcode and hasPostcode columns
    data = data.drop(columns=['postcode', hasPostcodeField])

    return data

def truncate_date(series):
    # Convert and round the date
    return pd.DatetimeIndex(series).tz_localize(None).floor('D')

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

    data = geo_match(data)

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


def pull_group_entries():
    data = pull_collection(
        collection_name=u'form-builder-submissions/groupBallotEntry/responses',
        fields=[
            'dateSubmitted',
            'postcodeSkipped',
            'postcode',
            'noTickets',
        ])

    data = data.loc[~data.noTickets.isna()]

    data = data.rename(columns={
        'dateSubmitted': 'date_submitted',
        'noTickets': 'count_of_tickets',
    })

    data['hasPostcode'] = ~data.postcodeSkipped

    data = geo_match(data)
    data.date_submitted = truncate_date(data.date_submitted)

    data[[
        'date_submitted',
        'la_code',
        'ward_code',
        'count_of_tickets',
    ]].sort_values(
      by=['date_submitted']
    ).to_csv(
      RAW_GROUP_DATA,
      index=False
    )


if __name__ == '__main__':
    update()
    pull_group_entries()
