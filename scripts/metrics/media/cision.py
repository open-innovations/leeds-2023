import datetime
import glob
import logging
import os

import chardet
import pandas as pd

TOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
LOG_DIR = os.path.join(TOP_DIR, 'working/log')
WORKING_DIR = os.path.join(TOP_DIR, 'working/manual/media')
OUTPUT_DIR = os.path.join(TOP_DIR, 'data/metrics/media_coverage')

LATEST_DATE = datetime.datetime.now()
HASH_KEY = "2023202320232023"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_fh = logging.FileHandler(filename=os.path.join(
    LOG_DIR, "media_cision.log"), mode="w")
log_formatter = logging.Formatter('%(levelname)s:%(funcName)s:%(message)s')
log_fh.setFormatter(log_formatter)
logger.addHandler(log_fh)


def load_cision_files():
    files = list_cision_files()

    dfs = pd.concat([load_cision_file(file) for file in files])
    return dfs.pipe(clean_up)


def list_cision_files():
    '''
    List the available CSV files
    '''
    return glob.glob(os.path.join(WORKING_DIR, '*.csv'))


def load_cision_file(filepath):
    logger.info('Loading %s', filepath)
    return (
        pd.read_csv(filepath, encoding=guess_encoding(filepath), thousands=',')
          # .pipe(append_filename, os.path.basename(filepath))
          .pipe(normalise_column_names)
          .pipe(patch_column_names)
          .pipe(drop_empty_headlines)
          .pipe(guess_date)
          .pipe(convert_numbers)
          .pipe(add_hash)
    )


def guess_encoding(file):
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def append_filename(data, filename):
    data['source_file'] = filename
    return data


def normalise_column_names(data):
    '''
    Normalise names of columns
    '''
    data.columns = data.columns\
        .str.strip()\
        .str.replace(' ', '_')\
        .str.replace('*', '', regex=False)\
        .str.lower()
    return data


def patch_column_names(data):
    return data.rename(columns={
        'headline': 'news_headline',
        'date': 'news_date',
        'uvpm': 'uv',
        'circulation': 'audience_reach',
        'circ.': 'audience_reach',
        'publication': 'outlet_name'
    })


def drop_empty_headlines(data):
    '''
    Drop rows with empty news headline (Cision has started adding a footer)
    '''
    return data[~data['news_headline'].isna()]


def guess_date(data):
    known_formats = [
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d/%m/%y",
        "%d.%m.%y",
        "%d-%b"
    ]

    # Construct a data frame of all potential dates
    dates = pd.concat(
        [pd.to_datetime(data.news_date, format=f, errors='coerce')
         for f in known_formats],
        axis=1
    )

    # Get rid of any dates in the future
    dates[dates.news_date > pd.Timestamp.now()] = pd.NaT

    # Backfill and take the first column
    dates = dates.bfill(axis=1).iloc[:, 0]

    # Handle any dates far into the past
    dates = dates.mask(dates.dt.year < 2022, dates + pd.offsets.DateOffset(year=2023))

    if len(dates[dates.isna()]) > 1:
        logger.error('Some incompatible date formats found')
        return pd.DataFrame(columns=data.columns)

    data['news_date'] = dates
    return data


def convert_numbers(data):
    # Convert viewship to int
    try:
        data['uv'] = data['uv'].fillna(0).astype('Int64')
    except Exception as e:
        logger.error(e)
        data['uv'] = pd.to_numeric(
            data['uv'].str.strip().str.replace(',', ''), errors="coerce"
        ).astype('Int64')

    # Convert reach to int
    try:
        data['audience_reach'] = data['audience_reach'].fillna(
            0).astype('Int64')
    except Exception as e:
        logger.error(e)
        data.audience_reach = pd.to_numeric(
            data.audience_reach.str.strip().str.replace(',', ''), errors="coerce"
        ).astype('Int64')

    return data


def add_hash(data):
    # Add identifier
    data['hash'] = pd.util.hash_pandas_object(
        data[['news_date', 'news_headline', 'outlet_name']], hash_key=HASH_KEY, index=False)
    return data



def clean_up(data):
    data = data.drop(
        columns=['news_text', 'contact_name', 'news_attachment_name'], errors='ignore'
    ).sort_values(
        by=['news_date', 'news_headline', 'medium']
    )
    return data


def save_csv(data, output_file):
    # Set columns order
    columns_order = ['news_date', 'news_headline', 'outlet_name', 'audience_reach',
                     'uv', 'tone', 'medium', 'outlet_type', 'custom_tags', 'news_company_mentions',
                     'hash',
                    #  'source_file'
                     ]
    data = data.reindex(columns=columns_order)

    data.sort_values(by=['news_date', 'news_headline', 'outlet_name', 'medium']).to_csv(
        output_file, index=False)
    return data


