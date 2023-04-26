import os
import pandas as pd
from extract import STAGING_DIR
import util.geography as geo

DATA_DIR = 'data/metrics/community-grants/'
os.makedirs(DATA_DIR, exist_ok=True)

RESPONSE_CSV = os.path.join(DATA_DIR, 'responses.csv')


def key_map(value):
    return {
        'my_leeds_grant_app_audiovisual': 'my_leeds_grant_app',
    }.get(value, value);


if __name__ == '__main__':
    grants = os.listdir(STAGING_DIR)
    data = pd.DataFrame()

    # Load each file add a key and append to the big result data frame
    for filename in grants:
        key = key_map(filename.replace(r".csv", ""))
        grant_data = pd.read_csv(os.path.join(STAGING_DIR, filename))
        grant_data['grant'] = key
        data = pd.concat([data, grant_data])

    # Do the ward match
    data = geo.match_la(data)
    data = geo.match_ward(data)
    data = data.drop(columns=['postcode'])

    # Save to csv
    data.sort_values(by=[
        'date_submitted',
        'la_code',
        'ward_code',
    ]).to_csv(RESPONSE_CSV, index=False)
