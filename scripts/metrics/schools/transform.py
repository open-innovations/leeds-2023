import os
import re
import pandas as pd

from util.geography import fuzzy_match_ward_name_to_code

from extract import SCHOOLS_DATA as RAW_SCHOOLS_DATA

DATA_DIR = os.path.join("data", "metrics", "schools")
os.makedirs(DATA_DIR, exist_ok=True)
SCHOOLS_DATA = os.path.join(DATA_DIR, 'schools_engagement.csv')


def transform(data):
    data['Ward'] = data['Ward'].str.strip()
    data = fuzzy_match_ward_name_to_code(data, ward_name_col='Ward')
    data = data.drop(columns=['Ward'])
    data = data.rename(columns={
        'Total engagements': 'total_engagements',
        'Total number of learners ': 'total_number_of_learners'
    })

    data = data.groupby('ward_code').sum().astype(int)
    data = data.reset_index()

    return data


if __name__ == '__main__':
    data = pd.read_csv(RAW_SCHOOLS_DATA)
    data.rename(columns=lambda x: re.sub(
        r"\W+", '_', x.lower()).strip('_'), inplace=True)
    data.to_csv(SCHOOLS_DATA, index=False)
