import os
import re

import pandas as pd
from thefuzz import process

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '../../')

LEEDS_WARDS_CSV = os.path.join(os.path.dirname(
    __file__), '../../data/reference/leeds_wards.csv')
POSTCODE_CSV = os.path.join(PROJECT_ROOT, 'data/reference/postcodes.csv')

leeds_wards = pd.read_csv(LEEDS_WARDS_CSV)


def normalise_leeds_wards(input):
    valid = input.notna()
    result = pd.Series(data=pd.NA, index=input.index, dtype='string')
    result.loc[valid] = input.loc[valid].apply(
        lambda x: process.extractOne(x, leeds_wards.WD21NM)[0]
    )
    return result


def ward_name_to_code(input):
    return input.map(leeds_wards.set_index('WD21NM').WD21CD.to_dict())


def ward_code_to_name(input):
    return input.map(leeds_wards.set_index('WD21CD').WD21NM.to_dict())


def load_postcodes(columns=None):
    return pd.read_csv(POSTCODE_CSV, usecols=columns)


def postcode_formatter(series):
    def format(postcode):
        if postcode is not None:
            postcode = re.sub(
                r'^([A-Z]+)(\d+)\s*(\d)([A-Z]{2})', r'\1\2 \3\4', str(postcode).upper().strip().replace(' ', ''))
            return postcode
    return series.apply(format)

ward_data = load_postcodes(columns=['pcds', 'osward', 'oslaua'])

postcode_to_ward_code = ward_data[['pcds', 'osward']].drop_duplicates(


).set_index('pcds').osward.to_dict()

postcode_to_la_code = ward_data[['pcds', 'oslaua']].drop_duplicates(
).set_index('pcds').oslaua.to_dict()

ward_code_to_la_code = ward_data[['osward', 'oslaua']].drop_duplicates(
).set_index('osward').oslaua.to_dict()
