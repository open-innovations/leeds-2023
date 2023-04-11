import pandas as pd
import numpy as np
import os 

WORKING_DIR = os.path.join('working')
SCHOOLS_DIR = os.path.join(WORKING_DIR, 'tracker.csv')
SUMMARY_DIR = os.path.join('docs', 'metrics', 'schools', '_data', 'schools_summary.csv')

SCHOOLS_DATA = os.path.join(WORKING_DIR, 'all_schools_list.csv')

def fetch_data(): 
    list = pd.read_csv(SCHOOLS_DIR, usecols=['School_name', 'Ward', 'Total engagements', 'Total number of learners'])
    list = list[:-2].fillna(0.0)
    schools_list = pd.DataFrame({
        'school_name': list.School_name,
        'ward': list.Ward,
        'total_engagements': list['Total engagements'].astype(int),
        'total_learners': list['Total number of learners'].astype(int),
    })
    schools_list.to_csv(SCHOOLS_DATA, index=False)

def prepare():
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

if __name__ == '__main__':
    fetch_data()
    prepare()