import pandas as pd
import os

RAW_DATA_DIR = os.path.join('working', 'manual', 'media')
HISTORIC_PATH = os.path.join(RAW_DATA_DIR, 'Leeds 2023 AVE.xlsx')
CISION_PATH = os.path.join(
    RAW_DATA_DIR, 'Cision - Leeds 2023 23 Sept - 17 Oct for OI.csv')
OUTPUT_PATH = os.path.join(
    'data', 'metrics', 'media_coverage', 'combined_historic.csv')


def load_20_21():
    columns = ['Tier', 'Outlet Name', 'News Date',
               'News Headline', 'Type', 'Custom Tags', 'Medium', 'Audience Reach']
    data = pd.read_excel(HISTORIC_PATH, usecols='A:H', nrows=217,
                         sheet_name='April 2020-July 2021', names=columns, parse_dates=['News Date'])
    data['Medium'] = data['Medium'].str.capitalize()

    return data


def load_21_22():
    columns = ['Outlet Name', 'News Headline', 'News Date', 'Type',
               'Messaging', 'Tone', 'Custom Tags', 'Tier', 'Medium', 'Audience Reach']
    data = pd.read_excel(HISTORIC_PATH, usecols='A:J', nrows=335,
                         sheet_name='Aug 2021 - July 2022', names=columns, parse_dates=['News Date'])
    data['Tone'] = data['Tone'].replace(
        {'\s*Positive\s*': 'POS', '\s*Negative\s*': 'NEG', '\s*Neutral\s*': 'NEU'}, regex=True)

    return data


if __name__ == '__main__':
    historic_data_20_21 = load_20_21()
    historic_data_21_22 = load_21_22()
    # cision_data = pd.read_csv(CISION_PATH,parse_dates=['News Date'],dayfirst=True)

    columns_order = ['News Date', 'News Headline', 'Outlet Name',
                     'Audience Reach', 'Tone', 'Medium', 'Custom Tags']

    # Drop columns and sort by date
    combined_data = (pd.concat([
        historic_data_20_21,
        historic_data_21_22,
    ]).drop(columns=['Tier', 'Type', 'Messaging',])
      .sort_values(by=['News Date', 'News Headline', 'Medium'])
      .reindex(columns=columns_order)
    )

    # change column types
    combined_data['Audience Reach'] = combined_data['Audience Reach'].astype(
        'string').str.replace(',|\s|\.0|N/A', '', regex=True).replace('', None).astype('Int64')
    # combined_data['UV*'] = combined_data['UV*'].astype('Int64')

    # change column names
    combined_data.columns = combined_data.columns.str.replace(
        ' ', '_').str.replace('*', '', regex=False).str.lower()

    # strip string columns
    df_obj = combined_data.select_dtypes(['object'])
    combined_data[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    # Change to title case
    combined_data['custom_tags'] = combined_data['custom_tags'].str.title()

    combined_data.to_csv(OUTPUT_PATH, index=False)
