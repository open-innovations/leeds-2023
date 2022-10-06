import os

import pandas as pd
from metrics.ballot.firebase import get_db
from util.postcode import match_ward

DATA_DIR = os.path.join('data', 'metrics', 'ballot')
RAW_DATA = os.path.join(DATA_DIR, 'ballot_entries.csv')


def map_doc_to_dict(doc):
    dict = doc.get([
        'dateSubmitted',
        'postcode',
        'artistAgeGroup',
        'artworkMedium',
        'advertisingSource'
    ])
    print(dict)


def get_data():
    db = get_db()
    ballot_ref = db.collection(u'ballot-data')

    docs = ballot_ref.select([
        'dateSubmitted',
        'postcode',
        'artistAgeGroup',
        'artworkMedium',
        'advertisingSource'
    ]).stream()

    # Create a dataframe
    data = pd.DataFrame([doc.to_dict() for doc in docs])

    # Map postcode to ward
    data = match_ward(data)
    data = data.drop(columns=['postcode'])

    # Rename columns
    data = data.rename(columns={
        'dateSubmitted': 'date_submitted',
        'artistAgeGroup': 'artist_age_group',
        'artworkMedium': 'artwork_medium',
        'advertisingSource': 'advertising_source'
    })

    # Convert and round the date
    data.date_submitted = pd.DatetimeIndex(
        data.date_submitted).tz_localize(None).floor('D')

    return data


def save_raw_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    data.sort_values(
        by='date_submitted'
    ).to_csv(
        RAW_DATA, index=False
    )


def update():
    data = get_data()
    save_raw_data(data)
