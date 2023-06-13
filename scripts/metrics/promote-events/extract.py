import os
from scripts.util.logger import logging, log_formatter
from lib.sources.airtable import promote


logger = logging.getLogger('promote-events.extract')
log_handler = logging.FileHandler(
    'working/log/promote_events_extract.log', mode='w', encoding='utf-8')
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.info('Set up logging')

WORKING_DIR = os.path.join('working', 'metrics', 'promote-events')
EVENTS_SOURCE_DATA = os.path.join(WORKING_DIR, 'events.csv') 


if __name__ == "__main__":
    os.makedirs(WORKING_DIR, exist_ok=True)
    try:
        data = promote(
            view='Grid view',
            fields=[
              'Event Name',
              'Event Start Date',
              'Event End Date',
              'Venue - including address',
              'Stage',
              'Live date',
            ])

        data.to_csv(EVENTS_SOURCE_DATA, index=False)
    except Exception as e:
        logger.error(repr(e))
        raise RuntimeError('Cannot extract promote events data')
