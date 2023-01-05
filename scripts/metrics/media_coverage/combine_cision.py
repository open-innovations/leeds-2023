import pandas as pd
import os
import glob

WORKING_DIR = os.path.join('working', 'manual', 'media')
OUTPUT_FILE_PATH = os.path.join(
    'data', 'metrics', 'media_coverage', 'combined_cision.csv')
HASH_KEY = "2023202320232023"


def load_new_file(filepath):
    data = pd.read_csv(filepath)

    # Normalise names of columns
    data.columns = data.columns.str.replace(
        ' ', '_').str.replace('*', '', regex=False).str.lower()

    # Drop rows with empty news headline (Cision has started adding a footer)
    data = data[~data['news_headline'].isna()]

    # Convert news date into datetime format
    try:
        data['news_date'] = pd.to_datetime(
            data['news_date'], format="%d/%m/%Y")
        # If date before 2022-09-17 or after today, something is fishy
        # TODO implement this
    except:
        # Sometimes it's in MM/DD/YYYY format!
        data['news_date'] = pd.to_datetime(
            data['news_date'], format="%m/%d/%Y")

    # Convert viewship to int
    data['uv'] = data['uv'].astype('Int64')

    # Add identifier
    data['hash'] = pd.util.hash_pandas_object(
        data[['news_date', 'news_headline', 'outlet_name']], hash_key=HASH_KEY, index=False)

    return data


def combine_new_data(dfs):
    # Set columns order
    columns_order = ['news_date', 'news_headline', 'outlet_name', 'audience_reach',
                     'uv', 'tone', 'medium', 'outlet_type', 'custom_tags', 'news_company_mentions', 'hash']

    # Concatenate all data
    data = (pd.concat(dfs)
            .drop(columns=['news_text', 'contact_name', 'news_attachment_name'])
            .sort_values(by=['news_date', 'news_headline', 'medium'])
            .reindex(columns=columns_order))

    return data


if __name__ == '__main__':
    # Getting list of files
    files = glob.glob(os.path.join(WORKING_DIR, '*.csv'))

    # Load each file into a list of data frames
    dfs = [load_new_file(file) for file in files]

    # Concatenate all data
    combined_data = combine_new_data(dfs)

    # TODO Do a combine_first with existing data - unique key needed

    # Save to file
    combined_data.sort_values(by=['news_date', 'news_headline', 'outlet_name', 'medium']).to_csv(
        OUTPUT_FILE_PATH, index=False)
