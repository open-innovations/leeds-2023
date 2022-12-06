import os
import pandas as pd
from extract import STAGING_DIR
import util.geography as geo

DATA_DIR = 'data/metrics/callouts/'
os.makedirs(DATA_DIR, exist_ok=True)

RESPONSE_CSV = os.path.join(DATA_DIR, 'responses.csv')


if __name__ == '__main__':
    callouts = os.listdir(STAGING_DIR)
    data = pd.DataFrame()

    # Load each file add a key and append to the big result data frame
    for filename in callouts:
        key = filename.replace(r".csv", "")
        callout = pd.read_csv(os.path.join(STAGING_DIR, filename))
        callout['callout'] = key
        data = pd.concat([data, callout])

    # Do the ward match
    data = geo.match_la(data)
    data = geo.match_ward(data)
    data = data.drop(columns=['postcode'])

    # Save to csv
    data.sort_values(by=[
        'date_submitted',
        'callout',
        'la_code',
        'ward_code',
    ]).to_csv(RESPONSE_CSV, index=False)
