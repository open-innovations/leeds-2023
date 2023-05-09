import os
import pandas as pd
from extract import STAGING_DIR
import util.geography as geo
from util.logger import logging

logger = logging.getLogger('metrics.community-grants')

DATA_DIR = 'data/metrics/community-grants/'
os.makedirs(DATA_DIR, exist_ok=True)

RESPONSE_CSV = os.path.join(DATA_DIR, 'responses.csv')


def key_map(value):
    return {
        'my_leeds_grant_app_audiovisual': 'my_leeds_grant_app',
    }.get(value, value)


if __name__ == '__main__':
    grants = os.listdir(STAGING_DIR)
    data = pd.DataFrame()

    # Load each file add a key and append to the big result data frame
    for filename in grants:
        key = key_map(filename.replace(r".csv", ""))
        grant_data = pd.read_csv(os.path.join(STAGING_DIR, filename))
        grant_data['grant'] = key
        data = pd.concat([data, grant_data])
    
    data = data.reset_index(drop=True)
    
    # Do the ward match
    mapped_wards = data.ward.apply(geo.normalise_leeds_ward).map(geo.leeds_ward_name_to_code)
    mapped_wards.loc[mapped_wards.isna()] = data.postcode.loc[mapped_wards.isna()].apply(geo.postcode_formatter).map(geo.postcode_to_ward_code)
    unmapped_grants = data.date_submitted.count() - mapped_wards.count()
    try:
        assert unmapped_grants == 0, 'Have not been able to map all grants - {0} missing ward codes'.format(unmapped_grants)
    except AssertionError as e:
        logger.warning(e)
        print(data[mapped_wards.isna()])

    data['la_code'] = mapped_wards.map(geo.ward_code_to_la_code).fillna('UNKNOWN')
    data['ward_code'] = mapped_wards.fillna('UNKNOWN')
    data.type = data.type.str.lower().map({
        'communitygroup': 'community_group',
        'individual': 'individual',
        'voluntarygroup': 'voluntary_group',
        'organisation': 'organisation',
        'other': 'other',
        'artsorg': 'arts_organisation'
    })
    data = data.drop(columns=['id', 'postcode', 'ward'])

    # Save to csv
    data.sort_values(by=[
        'date_submitted',
        'la_code',
        'ward_code',
    ]).to_csv(RESPONSE_CSV, index=False)
