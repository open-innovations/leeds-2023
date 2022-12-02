import os
import logging
from util.firebase import pull_collection

EXTRACT_DIR=os.path.join('working', 'ballot')
INDIVIDUAL_RAW=os.path.join(EXTRACT_DIR, 'individual_ballots.csv')

def extract_individual():
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

    # Filter out entries wit missing submission date
    data = data.loc[~data.dateSubmitted.isna()]

    logging.info("Got %d entries", data.shape[0])

    os.makedirs(EXTRACT_DIR, exist_ok=True)
    data.to_csv(INDIVIDUAL_RAW)

if __name__ == '__main__':
    extract_individual()