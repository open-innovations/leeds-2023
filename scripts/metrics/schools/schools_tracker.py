import pandas as pd
import numpy as np
import os 

WORKING_DIR = os.path.join('working')
SCHOOLS_DIR = os.path.join(WORKING_DIR, 'tracker.csv')
SUMMARY_DIR = os.path.join('docs', 'metrics', 'schools', '_data', 'schools_summary.csv')

SCHOOLS_DATA = os.path.join(WORKING_DIR, 'all_schools_list.csv')
WARD_REFERENCE = os.path.join('data', 'reference', 'leeds_wards.csv')
MERGED_DATA = os.path.join('docs', 'metrics', 'schools', '_data', 'engagements_by_ward.csv')


def fetch_data(): 
    data = pd.read_csv(SCHOOLS_DIR, usecols=['School_name', 'Ward', 'Total engagements', 'Total number of learners'])
    data = data[:-2].fillna(0)
    schools = pd.DataFrame({
        'school_name': data.School_name,
        'ward': data.Ward,
        'total_engagements': data['Total engagements'].astype(int),
        'total_learners': data['Total number of learners'].astype(int),
    })
    schools = clean_wardnames(schools)
    schools.to_csv(SCHOOLS_DATA, index=False)


def prepare_summary():
    data = pd.read_csv(SCHOOLS_DATA)
    engagements = np.count_nonzero(data['total_engagements'], axis=0)
    total = len(data) 
    percentage_engaged = (engagements/total)*100
    summary = pd.DataFrame([
        total, 
        engagements, 
        percentage_engaged
    ], index=[
        "total_schools", 
        "total_engagements", 
        "percentage_engaged"
    ], columns=[
        "value"
    ]).round(0).astype(int)
    summary.to_csv(SUMMARY_DIR)


def clean_wardnames(data):
    data.ward = data.ward.str.replace('&', 'and')
    data.ward = data.ward.str.strip()
    data.ward = data.ward.str.replace('Bramley andStanningley', 'Bramley and Stanningley')
    data.ward = data.ward.str.replace('Adel and Wharfedale', 'Adel and Wharfdale')
    data.ward = data.ward.str.replace('Crossgates and Whinmoor', 'Cross Gates and Whinmoor')
    return data

def match_ward(data, ward_data, ward_name='ward'):
    data = data.merge(
        how='left',
        right=ward_data,
        left_on=ward_name,
        right_on='WD21NM',
        validate='many_to_one',
    )
    data = data[['WD21NM', 'WD21CD', 'total_engagements']]
    data.WD21NM.fillna('UNKNOWN', inplace=True)
    data.WD21CD.fillna('UNKNOWN', inplace=True)
    return data

def map_wards(): 
    engagements = pd.read_csv(SCHOOLS_DATA, usecols = ['ward', 'total_engagements'])
    leeds_wards = pd.read_csv(WARD_REFERENCE)
    merged = match_ward(engagements, leeds_wards)
    merged.to_csv(MERGED_DATA, index=False)


if __name__ == '__main__':
    fetch_data()
    prepare_summary()
    map_wards()
    