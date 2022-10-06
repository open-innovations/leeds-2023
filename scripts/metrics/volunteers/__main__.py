import logging

logging.basicConfig(
    format='%(asctime)s|%(levelname)s|%(message)s',
    encoding='utf-8',
    level=logging.DEBUG
)

import metrics.volunteers.process
import util.oi_sftp_server


logging.info('Processing volunteers...')
util.oi_sftp_server.get('rosterfy/current-checkpoint.csv', 'working/rosterfy/current-checkpoint.csv')
metrics.volunteers.process.update()
metrics.volunteers.process.summarise()
logging.info('Done!')
