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

logging.basicConfig(
  level=logging.WARNING
)

def load_new_file(filepath):
    data = pd.read_csv(filepath)

    # Normalise names of columns
    data.columns = data.columns.str.strip().str.replace(
        ' ', '_').str.replace('*', '', regex=False).str.lower()

    # Drop rows with empty news headline (Cision has started adding a footer)
    data = data[~data['news_headline'].isna()]

    # Convert news date into datetime format
    try:
        dates = pd.to_datetime(
            data['news_date'], format="%d/%m/%Y")
        # If date after today, something is fishy
        # TODO implement this
        unexpected = data[dates > LATEST_DATE]
        if len(unexpected) > 0:
            raise ValueError('Future date')
        data['news_date'] = dates
    except:
        logging.warning('File %s is in MM/DD/YYYY format', filepath)
        # Sometimes it's in MM/DD/YYYY format!
        data['news_date'] = pd.to_datetime(
            data['news_date'], format="%m/%d/%Y")

    # Convert viewship to int
    try:
        data['uv'] = data['uv'].astype('Int64')
    except:
        data['uv'] = pd.to_numeric(data['uv'].str.strip().str.replace(',', ''), errors="coerce").astype('Int64')

    # Convert reach to int
    try:
        data['audience_reach'] = data['audience_reach'].astype('Int64')
    except:
        data.audience_reach = pd.to_numeric(data.audience_reach.str.strip().str.replace(',', ''), errors="coerce").astype('Int64')

    # Add identifier
    data['hash'] = pd.util.hash_pandas_object(
        data[['news_date', 'news_headline', 'outlet_name']], hash_key=HASH_KEY, index=False)

    return data


def combine_new_data(dfs):
    # Concatenate all data
    data = (pd.concat(dfs)
            .drop(columns=['news_text', 'contact_name', 'news_attachment_name'], errors='ignore')
            .sort_values(by=['news_date', 'news_headline', 'medium']))

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

    # Load each file into a list of data frames
    dfs = [load_new_file(file) for file in files]

    # Concatenate all data
    combined_data = combine_new_data(dfs)

    # TODO Do a combine_first with existing data - unique key needed
    # THIS DOES NOT QUITE WORK
    # combined_data = update_existing(combined_data)

    # Save to file
    save_combined(combined_data)

    # Write out some summary stats
    weekly = combined_data.groupby('news_date').news_headline.count().resample('W-FRI').sum()
    weekly.to_csv(os.path.join(LOG_DIR, 'cision.csv'))


if __name__ == '__main__':
    transform()
