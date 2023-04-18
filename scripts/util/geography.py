import os
import re
import pandas as pd

from thefuzz import process

LEEDS_LA_CODE = 'E08000035'


def load_postcodes(columns=None):
    return pd.read_csv(os.path.join('data', 'reference', 'postcodes.csv'), usecols=columns)


def load_wards_2021():
    wards = pd.read_csv(os.path.join('data', 'reference', 'Wards_(December_2021)_GB_BFC.csv'), usecols=['WD21CD','WD21NM','LAT','LONG'])
    return wards


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


def local_authority_stats(codes, counts):
    data = pd.DataFrame(data={'counts': counts}, index=codes)
    data['segment'] = 'OUTSIDE_LEEDS'
    data.loc[LEEDS_LA_CODE, 'segment'] = 'Leeds'
    data.loc['UNKNOWN', 'segment'] = 'UNKNOWN'
    data.loc['NOT_PROVIDED', 'segment'] = 'NOT_PROVIDED'
    data = pd.DataFrame({
        'counts': data.groupby('segment').counts.sum()
    })
    return data.counts


def fuzzy_match_ward_name_to_code(data, ward_name_col="ward", ward_code_col="ward_code"):
    wards = load_wards_2021()
    wards = wards[
      (wards.LAT > 53) &
      (wards.LAT < 54) &
      (wards.LONG > -1.69) &
      (wards.LONG < -1.3)
    ]
    data['WD21NM'] = data[ward_name_col].apply(
      lambda x: process.extractOne(x, wards.WD21NM)[0])
    data = pd.merge(left=data, right=wards, on='WD21NM')
    data = data.drop(columns=[ward_name_col, 'LONG', 'LAT'])
    data = data.rename(columns={
      'WD21CD': ward_code_col,
      'WD21NM': ward_name_col
    })
    return data


def fuzzy_match_leeds_wards(data, ward_name_col="ward", ward_code_col="ward_code"):
    wards = pd.read_csv('data/reference/leeds_wards.csv')
    valid_wards = data[ward_name_col].notna()
    data.loc[valid_wards, 'WD21NM'] = data.loc[valid_wards, ward_name_col].apply(
        lambda x: process.extractOne(x, wards.WD21NM)[0])
    data = pd.merge(left=data, right=wards, how='left', on='WD21NM')
    data = data.drop(columns=[ward_name_col])
    data = data.rename(columns={
        'WD21CD': ward_code_col,
        'WD21NM': ward_name_col
    })
    return data
