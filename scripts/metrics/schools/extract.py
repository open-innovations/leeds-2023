import os
from pyairtable import Table
from pyairtable.formulas import match
import pandas as pd

API_KEY = os.environ['AIRTABLE_API_KEY']

WORKING_DIR = os.path.join('working', 'metrics', 'airtable')
os.makedirs(WORKING_DIR, exist_ok=True)

SCHOOLS_DATA = os.path.join(WORKING_DIR, 'schools_events.csv')

def fetch_data():
    BASE_ID = 'appHAh7IYG6p2w5Yo'
    TABLE_NAME = 'EVENTS'

    table = Table(API_KEY, BASE_ID, TABLE_NAME)

    school_events = table.all(
        fields=[
            'Event Unique Identifier',
            'Event name',
            'Project name',
            'Workstream',
            'Event type',
            'Season',
            'Start date',
            'End date',
            'Postcode (from Venue)',
            'Ward (from Venue)',
            'CLE - Setting',
            'CLE - Key Stage',
            'CLE - Subject Area',
            'CLE - Activity Type',
            'CLE - School Timing',
            'School Name (from School)',
            'School Address Postcode',
            'Ward (from School)',
            'Number of booked participants',
        ],
        formula=match({"Event type": "CLE - Creative Learning session"}),
    )
    return pd.json_normalize([x['fields'] for x in school_events])


if __name__ == '__main__':
    data = fetch_data()
    data.to_csv(SCHOOLS_DATA, index=False)
