import os
from pyairtable import Table
import pyairtable.formulas as f
import pandas as pd
from util.logger import logging, log_formatter

logger = logging.getLogger('schools.extract')
log_handler = logging.FileHandler('working/log/schools_extract.log', mode='w', encoding='utf-8')
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.info('Set up logging')

API_KEY = os.environ['AIRTABLE_API_KEY']

WORKING_DIR = os.path.join('working', 'metrics', 'airtable')
os.makedirs(WORKING_DIR, exist_ok=True)

SCHOOLS_DATA = os.path.join(WORKING_DIR, 'schools_events.csv')


def fetch_data():
    BASE_ID = 'appHAh7IYG6p2w5Yo'
    TABLE_NAME = 'EVENTS'
    VIEW_NAME = 'OI Creative Learning Evaluation Data'

    table = Table(API_KEY, BASE_ID, TABLE_NAME)

    school_events = table.all(
        view=VIEW_NAME,
        fields=['Event Unique Identifier',
                'Event name',
                'Project name',
                'Project type',
                'Event type',
                'Season',
                'Start date',
                'End date',
                'Postcode (from Venue)',
                'Ward (from Venue)',
                'ACTUAL Audience size / number of participants - IN PERSON',
                'ACTUAL Audience size / number of participants - ONLINE',
                'How many audience were teachers?',
                'CLE - Setting',
                'CLE - Key Stage',
                'CLE - Subject Area',
                'CLE - Activity Type',
                'CLE - School Timing',
                'School Name (from School)',
                'School Address Postcode',
                'Ward (from School)',
                'Number of booked participants',
                ])
    return pd.json_normalize([x['fields'] for x in school_events])


if __name__ == '__main__':
    try:
        data = fetch_data()
        data.to_csv(SCHOOLS_DATA, index=False)
    except Exception as e:
        logger.error(repr(e))
        raise RuntimeError('Cannot extract schools data')
