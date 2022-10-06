import logging

logging.basicConfig(
    format='%(asctime)s|%(levelname)s|%(message)s',
    encoding='utf-8',
    level=logging.DEBUG
)

import metrics.volunteers.process

logging.info('Processing volunteers...')
metrics.volunteers.process.update()
metrics.volunteers.process.summarise()
logging.info('Done!')
