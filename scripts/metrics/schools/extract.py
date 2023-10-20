from scripts.util.logger import logging, log_formatter


logger = logging.getLogger('schools.extract')
log_handler = logging.FileHandler(
    'working/log/schools_extract.log', mode='w', encoding='utf-8')
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.info('Set up logging')

import lib.sources.airtable as airtable
from config import RAW_SCHOOLS_DATA


def fetch_data():
    BASE_ID = 'appHAh7IYG6p2w5Yo'
    TABLE_NAME = 'EVENTS'
    VIEW_NAME = 'OI Creative Learning Evaluation Data'

    school_events = airtable.query(
        BASE_ID, TABLE_NAME,
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
    print(school_events)
    return school_events


if __name__ == '__main__':
    try:
        data = fetch_data()
        data.to_csv(RAW_SCHOOLS_DATA, index=False)
    except Exception as e:
        logger.error(repr(e))
        raise RuntimeError('Cannot extract schools data')
