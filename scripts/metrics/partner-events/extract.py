import os
from scripts.util.logger import logging, log_formatter
from lib.sources.airtable import events

logger = logging.getLogger('partner-events.extract')
log_handler = logging.FileHandler(
    'working/log/promote_events_extract.log', mode='w', encoding='utf-8')
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.info('Set up logging')

WORKING_DIR = os.path.join('working', 'metrics', 'partner-events')
EVENTS_SOURCE_DATA = os.path.join(WORKING_DIR, 'events.csv') 


if __name__ == "__main__":
    os.makedirs(WORKING_DIR, exist_ok=True)
    try:
        data = events(
            view='PARTNER programme',
            fields=[
              'Event name',
              'Project name',
              'Start date',
              'End date',
              'Ward (from Venue)',
              'ACTUAL Audience size / number of participants - IN PERSON',
              'ACTUAL Audience size / number of participants - ONLINE',
            ])
        data.to_csv(EVENTS_SOURCE_DATA, index=False)
    except Exception as e:
        logger.error(repr(e))
        raise RuntimeError('Cannot extract partner data')
