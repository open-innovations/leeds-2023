import os
import pandas as pd
from util.firebase import pull_collection


EXTRACT_DIR = os.path.join('working', 'ballot')
INDIVIDUAL_RAW = os.path.join(EXTRACT_DIR, 'individual_ballots.csv')
GROUP_RAW = os.path.join(EXTRACT_DIR, 'group_ballots.csv')


def extract_individual():
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

    os.makedirs(EXTRACT_DIR, exist_ok=True)
    data.to_csv(INDIVIDUAL_RAW, index=False)


def extract_group():
    data = pull_collection(
        collection_name=u'form-builder-submissions/groupBallotEntry/responses',
        fields=[
            'dateSubmitted',
            'postcodeSkipped',
            'postcode',
            'noTickets',
        ])

    data = data.loc[~data.noTickets.isna()]
    os.makedirs(EXTRACT_DIR, exist_ok=True)
    data.to_csv(GROUP_RAW, index=False)


def load_individual():
    return pd.read_csv(INDIVIDUAL_RAW)


def load_group():
    return pd.read_csv(GROUP_RAW)


if __name__ == '__main__':
    extract_individual()
    extract_group()
