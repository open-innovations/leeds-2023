import os

import pandas as pd

from pyairtable.formulas import match
from scripts.util.logger import logging, log_formatter
from lib.sources.airtable import query
from lib.util.convert import literal_converter


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
    formula = match({
        "cardPartnerBarTitle": "Beyond LEEDS 2023",
    })
    try:
        data = query(
            base_id='app40BfxSxQFxA3MC',
            table_name='tblIfvbra1m4vjm3O',
            formula=formula,
            fields=[
              'id',
              'name',
              'cardPrice',
              'cardPartnerBarTitle',
              'enableCardPartnerBar',
              'displayOnWebsite',
              'locationName',
              'timeslots',
              'Stage',
            ]
        )
        data.timeslots = data.timeslots.pipe(literal_converter)
        data = data.explode(['timeslots'])
        data.timeslots = pd.to_datetime(data.timeslots)
        data[
            (data.timeslots < pd.Timestamp.now()) &
            (data.timeslots > '2023-01-01')
        ].sort_index(axis=1).sort_values(['timeslots', 'id']).to_csv(EVENTS_SOURCE_DATA, index=False)
    except Exception as e:
        logger.error(repr(e))
        raise RuntimeError('Cannot extract promote events data')
