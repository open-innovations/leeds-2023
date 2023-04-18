import os
import re
import pandas as pd
from pyairtable import Table

API_KEY = os.environ['AIRTABLE_API_KEY']


def fetch_data():
    BASE_ID = 'appHAh7IYG6p2w5Yo'
    TABLE_NAME = 'Schools'

    table = Table(API_KEY, BASE_ID, TABLE_NAME)

    schools = table.all(
        fields=['School Name',
                'Postcode',
                'Ward',
        ])
    return pd.json_normalize([x['fields'] for x in schools]).rename(columns = lambda x: re.sub(r'\W+', '_', x.lower()))


if __name__ == '__main__':
    data = fetch_data()
    data.to_csv('data/reference/schools.csv', index=False)
