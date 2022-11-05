import pandas as pd

from util.geography import fuzzy_match_ward_name_to_code

def load_schools():
    data = pd.read_excel('working/School Engagement Tracker.xlsx',
      usecols=['Ward','Total engagements','Total number of learners '],
    )
    data = data[data.Ward.notna()]
    data['Ward'] = data['Ward'].str.strip()
    data = fuzzy_match_ward_name_to_code(data, ward_name_col='Ward')
    data = data.drop(columns=['Ward'])
    data = data.rename(columns={
      'Total engagements': 'total_engagements',
      'Total number of learners ': 'total_number_of_learners'
    })

    data = data.groupby('ward_code').sum().astype(int)
    data = data.reset_index()

    return data

def save_schools_data(data):
    data.to_csv('data/metrics/schools/schools_engagement.csv', index=False)