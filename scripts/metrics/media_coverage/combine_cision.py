import pandas as pd
import os
import glob
from hashlib import sha1

WORKING_DIR = os.path.join('working', 'manual', 'media')
OUTPUT_FILE_PATH = os.path.join(
    'data', 'metrics', 'media_coverage', 'combined_cision.csv')


def hash_string(value):
    return sha1(str(value).encode('utf-8')).hexdigest()


def set_hash_index(data):
    new_index = data.agg('{0[news_date]}{0[news_headline]}{0[outlet_name]}'.format, axis=1).apply(hash_string)
    data = data.set_index(new_index)
    return data


if __name__ == '__main__':
    # Getting list of files
    files = glob.glob(os.path.join(WORKING_DIR, '*.csv'))

    # Load each file into a list of data frames
    dfs = [pd.read_csv(file, parse_dates=['News Date'], dayfirst=True)
           for file in files]

    # Set columns order
    columns_order = ['News Date', 'News Headline', 'Outlet Name', 'Audience Reach',
                     'UV*', 'Tone', 'Medium', 'Outlet Type', 'Custom Tags', 'News Company Mentions']

    # Concatenate all data
    combined_data = (pd.concat(dfs)
                     .drop(columns=['News Text', 'Contact Name', 'News Attachment Name'], errors='ignore')
                     .sort_values(by=['News Date', 'News Headline', 'Medium'])
                     .reindex(columns=columns_order)
                     .drop_duplicates(subset=['News Date', 'News Headline', 'Medium','Outlet Name']))

    # Convert viewship to int
    combined_data['UV*'] = combined_data['UV*'].astype('Int64')

    # Normalise names of columns
    combined_data.columns = combined_data.columns.str.replace(
        ' ', '_').str.replace('*', '', regex=False).str.lower()

    # Combine new and existing data
    # Create a new hash index
    combined_data = set_hash_index(combined_data)
    
    # Read existing data and set hash index
    existing_data = pd.read_csv(OUTPUT_FILE_PATH, parse_dates=['news_date'], dtype={
      'uv': 'Int64',
    })

    existing_data = set_hash_index(existing_data)
    #existing_data = existing_data.drop_duplicates(subset=['news_date','outlet_name','news_headline'])
   
    # Combine, with the new data being priority
    combined_data = combined_data.combine_first(existing_data)

    # Save to file
    combined_data.sort_values(by=['news_date', 'news_headline', 'outlet_name', 'medium']).to_csv(OUTPUT_FILE_PATH, index=False)