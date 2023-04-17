import pandas as pd
import numpy as np
import os 

WORKING_DIR = os.path.join('working')
SCHOOLS_DIR = os.path.join(WORKING_DIR, 'tracker.csv')
SUMMARY_DIR = os.path.join('docs', 'metrics', 'schools', '_data', 'schools_summary.csv')

SCHOOLS_DATA = os.path.join(WORKING_DIR, 'all_schools_list.csv')
MISSING_SCHOOLS_DATA = os.path.join(WORKING_DIR, 'schools_to_add.csv')

ENGAGEMENTS_BY_WARD = os.path.join('docs', 'metrics', 'schools', '_data', 'engagements_by_ward.csv')
SCHOOL_ENGAGEMENT_COUNTS = os.path.join('docs', 'metrics', 'schools', '_data', 'school_engagement_counts.csv')

WARD_REFERENCE = os.path.join('data', 'reference', 'leeds_wards.csv')


def fetch_data(): 
    data = pd.read_csv(SCHOOLS_DIR, usecols=['School_name', 'Ward'])
    data = data[:-3].fillna(0)
    schools = pd.DataFrame({
        'school_name': data.School_name,
        'ward': data.Ward,
    })
    schools = clean_schools_data(schools)
    schools.to_csv(SCHOOLS_DATA, index=False)

def summarise():
    data = pd.read_csv(SCHOOLS_DATA)
    engagements = pd.read_csv(SCHOOL_ENGAGEMENT_COUNTS)

    school_engagements = len(engagements)

    total = len(data) 
    percentage_engaged = (school_engagements/total)*100
    summary = pd.DataFrame([
        total, 
        school_engagements, 
        percentage_engaged
    ], index=[
        "total_schools", 
        "school_engagements", 
        "percentage_engaged"
    ], columns=[
        "value"
    ]).round(0).astype(int)

    summary.to_csv(SUMMARY_DIR)

def clean_schools_data(data):
    data = clean_wardnames(data)
    data = add_missing_schools(data, pd.read_csv(MISSING_SCHOOLS_DATA))
    data = clean_schoolnames(data)
    return data

def clean_schoolnames(data):
    data.school_name = data.school_name.str.replace('Lowtown Primary School', 'Pudsey Lowtown Primary School')
    return data

def clean_wardnames(data):
    data.ward = data.ward.str.replace('&', 'and')
    data.ward = data.ward.str.strip()
    data.ward = data.ward.str.replace('Bramley andStanningley', 'Bramley and Stanningley')
    data.ward = data.ward.str.replace('Adel and Wharfedale', 'Adel and Wharfdale')
    data.ward = data.ward.str.replace('Crossgates and Whinmoor', 'Cross Gates and Whinmoor')
    data.ward = data.ward.str.replace('Middleton', 'Middleton Park')
    data.ward = data.ward.str.replace('Middleton Park Park', 'Middleton Park')
    data.ward = data.ward.str.replace('Weetwood Lane', 'Weetwood')
    return data

def add_missing_schools(data, missing_schools):
    combined = pd.concat( [data, missing_schools], ignore_index=True )
    return combined

def transform(): 
    all_schools = pd.read_csv(SCHOOLS_DATA, usecols = ['school_name', 'ward'])
    engagements = pd.read_csv(SCHOOL_ENGAGEMENT_COUNTS)
    leeds_wards = pd.read_csv(WARD_REFERENCE)

    engagements_all_schools = all_schools.merge(
        how='outer',
        right=engagements,
        left_on= 'school_name', 
        right_on='school',
        validate='many_to_many',
    )
    engagements_by_ward = leeds_wards.merge(
        how='outer',
        right=engagements_all_schools,
        left_on= 'WD21NM',
        right_on='ward',
        validate='one_to_many',
    ).drop(['school_name', 'ward', 'school'], axis=1)
    
    engagements_by_ward.count_of_engagements = engagements_by_ward.count_of_engagements.fillna(0).astype(int)
    engagements_by_ward.count_of_engagements = engagements_by_ward.groupby(
        'WD21NM')[
        'count_of_engagements'].transform('sum').fillna(0).astype(int)
    engagements_by_ward = engagements_by_ward.drop_duplicates(subset=['WD21NM'], keep='first')

    engagements_by_ward.to_csv(ENGAGEMENTS_BY_WARD, index=False)


if __name__ == '__main__':
    fetch_data()
    summarise()
    transform()
    