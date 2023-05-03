import logging

logging.basicConfig(
    format='%(asctime)s|%(levelname)s|%(pathname)s|%(message)s',
    encoding='utf-8',
    level=logging.INFO,
)

log_formatter = logging.Formatter('%(levelname)s:%(funcName)s:%(message)s')