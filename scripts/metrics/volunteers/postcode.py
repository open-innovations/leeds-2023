import os
import re
import pandas as pd


def load_postcodes():
    return pd.read_csv(os.path.join('data', 'reference', 'postcodes.csv'))


def postcode_formatter(postcode):
    if postcode is not None:
        postcode = re.sub(
            r'^([A-Z]+)(\d+)\s*(\d)([A-Z]{2})', r'\1\2 \3\4', str(postcode).upper().strip())
        return postcode


postcode_data = load_postcodes()


def lookup_ward_from_postcode(postcode):
    postcode = postcode_formatter(postcode)
    matches = postcode_data[postcode_data.pcds == postcode]
    # matches = postcode_data.query('pcds == @postcode')
    if (len(matches) < 1):
        return pd.NA
    return matches.osward.values[0]
