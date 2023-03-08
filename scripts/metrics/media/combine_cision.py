import pandas as pd
import os
import glob
from datetime import datetime
import logging


WORKING_DIR = os.path.join('working', 'manual', 'media')
OUTPUT_FILE_PATH = os.path.join(
    'data', 'metrics', 'media_coverage', 'combined_cision.csv')
HASH_KEY = "2023202320232023"

LOG_DIR = os.path.join('working', 'log')
os.makedirs(LOG_DIR, exist_ok=True)

LATEST_DATE = datetime.now()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_fh = logging.FileHandler(filename=os.path.join(
    LOG_DIR, "media_cision.log"), mode="w")
log_formatter = logging.Formatter('%(levelname)s:%(funcName)s:%(message)s')
log_fh.setFormatter(log_formatter)
logger.addHandler(log_fh)


def load_new_file(filepath):
    logger.info('Loading %s', filepath)
    data = pd.read_csv(filepath)

    # Normalise names of columns
    data.columns = data.columns.str.strip().str.replace(
        ' ', '_').str.replace('*', '', regex=False).str.lower()

    # Drop rows with empty news headline (Cision has started adding a footer)
    data = data[~data['news_headline'].isna()]

    known_formats = [
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d/%m/%y",
        "%d.%m.%y",
    ]
    # Convert news date into datetime format
    for format in known_formats:
        try:
            logger.info('Attemping to parse dates as %s', format)
            dates = pd.to_datetime(
                data['news_date'], errors='raise', format=format)
            unexpected = data[dates > LATEST_DATE]
            if len(unexpected) > 0:
                raise ValueError('Future date')
            logger.info('Looks like that worked!')
            break
        except:
            logger.warning('File %s is not in in %s format', filepath, format)

    try:
        data['news_date'] = dates
    except UnboundLocalError:
        logger.error(
            'File %s not processed, no compatible date formats found', filepath)
        # Dropping all data!
        return None

    # Convert viewship to int
    try:
        data['uv'] = data['uv'].astype('Int64')
    except:
        data['uv'] = pd.to_numeric(data['uv'].str.strip().str.replace(
            ',', ''), errors="coerce").astype('Int64')

    # Convert reach to int
    try:
        data['audience_reach'] = data['audience_reach'].astype('Int64')
    except:
        data.audience_reach = pd.to_numeric(data.audience_reach.str.strip(
        ).str.replace(',', ''), errors="coerce").astype('Int64')

    # Add identifier
    data['hash'] = pd.util.hash_pandas_object(
        data[['news_date', 'news_headline', 'outlet_name']], hash_key=HASH_KEY, index=False)

    return {
        'filename': os.path.basename(filepath),
        'data': data,
        'latest': data.news_date.max(),
        'earliest': data.news_date.min(),
    }


def combine_new_data(dfs):
    # Concatenate all data
    # Get the first data frame
    current = dfs.pop()
    data = current['data']
    logger.info('Processing data loaded from %s (%d records)',
                current['filename'], len(current['data']))

    # Iterate through the rest
    while len(dfs):
        # Find out what the current earliest one is
        earliest = data.news_date.min()
        # Get the next one
        current = dfs.pop()

        # TODO Remove likely duplicates
        # Filter the data frame so it excludes dates already processed
        # This does not work...
        # current['data'] = current['data'][current['data'].news_date < earliest]

        logger.info('Processing data loaded from %s (%d records)',
                    current['filename'], len(current['data']))

        # Concatenate the current and next data
        data = pd.concat([data, current['data']])

    # Clean up the data frame
    data = data.drop(
        columns=['news_text', 'contact_name', 'news_attachment_name'], errors='ignore'
    ).sort_values(
        by=['news_date', 'news_headline', 'medium']
    )

    return data


def update_existing(new_data):
    # Get list of known hashes
    hashes = new_data.hash.unique()

    # Load existing data
    existing_data = load_combined()

    # Find existing data that is (probably) not in the new data
    existing_data = existing_data[~existing_data.hash.isin(hashes)]

    # Combine hashes not in new data
    return pd.concat([existing_data, new_data])


def save_combined(data):
    # Set columns order
    columns_order = ['news_date', 'news_headline', 'outlet_name', 'audience_reach',
                     'uv', 'tone', 'medium', 'outlet_type', 'custom_tags', 'news_company_mentions', 'hash']
    data = data.reindex(columns=columns_order)

    data.sort_values(by=['news_date', 'news_headline', 'outlet_name', 'medium']).to_csv(
        OUTPUT_FILE_PATH, index=False)


def load_combined():
    data = pd.read_csv(OUTPUT_FILE_PATH, parse_dates=['news_date'])

    data['uv'] = data['uv'].astype('Int64')
    data['audience_reach'] = data['audience_reach'].astype('Int64')

    return data


def transform():
    # Getting list of files
    files = glob.glob(os.path.join(WORKING_DIR, '*.csv'))

    # If no files, nothing to do, so return
    if len(files) == 0:
        return

    # Load each file into a list of data frames - oldest first
    dfs = [df for df in (load_new_file(file) for file in files) if df != None]
    dfs = sorted(dfs, key=lambda i: (i['latest'], i['earliest']))

    # Concatenate all data
    combined_data = combine_new_data(dfs)

    # TODO Do a combine_first with existing data - unique key needed
    # THIS DOES NOT QUITE WORK
    # combined_data = update_existing(combined_data)

    # Save to file
    save_combined(combined_data)

    # Write out some summary stats
    weekly = combined_data.groupby(
        'news_date').news_headline.count().resample('W-FRI').sum()
    weekly.to_csv(os.path.join(LOG_DIR, 'cision.csv'))


if __name__ == '__main__':
    transform()
