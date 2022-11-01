import os
import re
import pandas as pd


def load_postcodes(columns=None):
    return pd.read_csv(os.path.join('data', 'reference', 'postcodes.csv'), usecols=columns)


def postcode_formatter(postcode):
    if postcode is not None:
        postcode = re.sub(
            r'^([A-Z]+)(\d+)\s*(\d)([A-Z]{2})', r'\1\2 \3\4', str(postcode).upper().strip().replace(' ', ''))
        return postcode


ward_data = load_postcodes(columns=['pcds', 'osward', 'oslaua'])


def match_ward(data, postcode_field='postcode', ward_column='ward_code'):
    data[postcode_field] = data[postcode_field].apply(postcode_formatter)
    data = data.merge(
        how='left',
        right=ward_data[['pcds', 'osward']],
        left_on=postcode_field,
        right_on='pcds',
        validate='many_to_one',
    )
    data.osward.fillna('UNKNOWN', inplace=True)
    data.drop(columns=['pcds'], inplace=True)
    data.rename(columns={'osward': ward_column}, inplace=True)
    return data


def match_geo(data, postcode_field, geo_field, rename_to=None):
    data[postcode_field] = data[postcode_field].apply(postcode_formatter)
    data = data.merge(
        how='left',
        right=ward_data[['pcds', geo_field]],
        left_on=postcode_field,
        right_on='pcds',
        validate='many_to_one',
    )
    data[geo_field].fillna('UNKNOWN', inplace=True)
    data.drop(columns=['pcds'], inplace=True)
    if rename_to != None:
        data.rename(columns={geo_field: rename_to}, inplace=True)
    return data


def match_la(data, postcode_field='postcode', la_column='la_code'):
    data = match_geo(data, postcode_field, 'oslaua', rename_to=la_column)
    return data
