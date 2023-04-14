import pandas as pd
import numpy as np
import os 

WORKING_DIR = os.path.join('working')
SCHOOLS_DIR = os.path.join(WORKING_DIR, 'tracker.csv')
SUMMARY_DIR = os.path.join('docs', 'metrics', 'schools', '_data', 'schools_summary.csv')

SCHOOLS_DATA = os.path.join(WORKING_DIR, 'all_schools_list.csv')
WARD_REFERENCE = os.path.join('data', 'reference', 'leeds_wards.csv')
MERGED_DATA = os.path.join('docs', 'metrics', 'schools', '_data', 'engagements_by_ward.csv')
SCHOOL_ENGAGEMENT_COUNTS = os.path.join('docs', 'metrics', 'schools', '_data', 'school_engagement_counts.csv')
ALL_ENGAGEMENTS = os.path.join(WORKING_DIR, 'all_engagements.csv')


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


def summarise():
    data = pd.read_csv(SCHOOLS_DATA)
    engagements = pd.read_csv(SCHOOL_ENGAGEMENT_COUNTS)
    engagements = engagements['count_of_engagements'].sum()
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

def clean_schools_data(data):
    data.school = data.school.str.replace('Pudsey Lowtown Primary School', 'Lowtown Primary School')
    return data

def clean_wardnames(data):
    data.ward = data.ward.str.replace('&', 'and')
    data.ward = data.ward.str.strip()
    data.ward = data.ward.str.replace('Bramley andStanningley', 'Bramley and Stanningley')
    data.ward = data.ward.str.replace('Adel and Wharfedale', 'Adel and Wharfdale')
    data.ward = data.ward.str.replace('Crossgates and Whinmoor', 'Cross Gates and Whinmoor')
    data.ward = data.ward.str.replace('Middleton', 'Middleton Park')
    data.ward = data.ward.str.replace('Middleton Park Park', 'Middleton Park')
    return data

def map_wards(): 
    all_schools = pd.read_csv(SCHOOLS_DATA, usecols = ['school_name', 'ward'])
    engagements = pd.read_csv(SCHOOL_ENGAGEMENT_COUNTS)
    clean_schools_data(engagements)
    leeds_wards = pd.read_csv(WARD_REFERENCE)
    engagements_all_schools = all_schools.merge(
        how='outer',
        right=engagements,
        left_on= 'school_name', 
        right_on='school',
        validate='many_to_many',
    )
    engagements_all_schools.to_csv(ALL_ENGAGEMENTS, index = False)
    engagements_by_ward = leeds_wards.merge(
        how='outer',
        right=engagements_all_schools,
        left_on= 'WD21NM',
        right_on='ward',
        validate='one_to_many',
    )
    engagements_by_ward.count_of_engagements = engagements_by_ward.count_of_engagements.fillna(0).astype(int)
    engagements_by_ward.count_of_engagements = engagements_by_ward.groupby(
        'WD21NM')[
        'count_of_engagements'].transform('sum').fillna(0).astype(int)
    engagements_by_ward = engagements_by_ward.drop_duplicates(subset=['WD21NM'], keep='first')
    engagements_by_ward.to_csv(MERGED_DATA, index=False)


if __name__ == '__main__':
    fetch_data()
    summarise()
    map_wards()
    