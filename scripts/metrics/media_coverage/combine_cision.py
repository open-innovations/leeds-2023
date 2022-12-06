import pandas as pd
import os
import glob

WORKING_DIR = os.path.join('working', 'manual', 'media')
OUTPUT_FILE_PATH = os.path.join(
    'data', 'metrics', 'media_coverage', 'combined_cision.csv')

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
                     .drop(columns=['News Text', 'Contact Name', 'News Attachment Name'])
                     .sort_values(by=['News Date', 'News Headline', 'Medium'])
                     .reindex(columns=columns_order))

    # Convert viewship to int
    combined_data['UV*'] = combined_data['UV*'].astype('Int64')

    # Normalise names of columns
    combined_data.columns = combined_data.columns.str.replace(
        ' ', '_').str.replace('*', '', regex=False).str.lower()

    # TODO Do a combine_first with existing data - unique key needed

    # Save to file
    combined_data.sort_values(by=['news_date', 'news_headline', 'outlet_name', 'medium']).to_csv(OUTPUT_FILE_PATH, index=False)
