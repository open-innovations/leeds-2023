import os
import pandas as pd
from thefuzz import process

LEEDS_WARDS_CSV = os.path.join(os.path.dirname(__file__), '../../data/reference/leeds_wards.csv')

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