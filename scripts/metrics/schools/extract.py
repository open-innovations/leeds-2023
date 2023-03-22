import os
from pyairtable import Table
import pyairtable.formulas as f
import pandas as pd

API_KEY = os.environ['AIRTABLE_API_KEY']

# FIND('CLE - Creative Learning session', {Event+type})
filter = f.FIND(f.to_airtable_value("CLE - Creative Learning session"), "ARRAYJOIN({Event type})")

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
            'ACTUAL Audience size / number of participants - IN PERSON',
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
        # FIND('CLE - Creative Learning session', {Event+type})
        formula=filter
    )
    return pd.json_normalize([x['fields'] for x in school_events])


if __name__ == '__main__':
    data = fetch_data()
    print(SCHOOLS_DATA)
    data.to_csv(SCHOOLS_DATA, index=False)
