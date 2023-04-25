import json
import os
import re
import ast

import pandas as pd
from extract import SCHOOLS_DATA as RAW_SCHOOLS_DATA
from util.geography import fuzzy_match_ward_name_to_code

DATA_DIR = os.path.join("data", "metrics", "schools")
os.makedirs(DATA_DIR, exist_ok=True)
SCHOOLS_DATA = os.path.join(DATA_DIR, 'schools_events.csv')


def literal_converter(series):
    def convert(value):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value
    return series.apply(convert)


def read_raw_data():
    # Load the file
    data = pd.read_csv(RAW_SCHOOLS_DATA).apply(func=literal_converter)

    # Slugify the column names
    data.rename(columns=lambda x: re.sub(
        r"\W+", '_', x.lower()).strip('_'), inplace=True)

    data.actual_audience_size_number_of_participants_in_person = data.actual_audience_size_number_of_participants_in_person.fillna(0)
    data.actual_audience_size_number_of_participants_online = data.actual_audience_size_number_of_participants_online.fillna(0)
    data.how_many_audience_were_teachers = data.how_many_audience_were_teachers.fillna(0)

    return data


def transform(data):
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


if __name__ == '__main__':
    data = read_raw_data()

    today = pd.Timestamp.today().floor('D')
    events = pd.DataFrame({
        'date': pd.to_datetime(data.start_date),
        'event_name': data.event_name,
        'project_type': data.project_type,
        'project_name': data.project_name,
        'venue_wards': data.ward_from_venue,
        'venue_postcodes': data.postcode_from_venue,
        'schools': data.school_name_from_school.fillna(''),
        'wards': data.ward_from_school,
        'postcodes': data.school_address_postcode,
        'participant_count': (data.actual_audience_size_number_of_participants_in_person + data.actual_audience_size_number_of_participants_online).fillna(0),
        'pupil_count': (data.actual_audience_size_number_of_participants_in_person + data.actual_audience_size_number_of_participants_online - data.how_many_audience_were_teachers).fillna(0),
        'teacher_count': data.how_many_audience_were_teachers.fillna(0),
    }).sort_values('date').query('~date.isna()').query('date < @today')

    print(data[[
        'actual_audience_size_number_of_participants_in_person',
        'actual_audience_size_number_of_participants_online',
        'how_many_audience_were_teachers',
    ]].describe())

    events['school_count'] = events.schools.map(len)

    # Save the schools data
    events.to_csv(SCHOOLS_DATA, index=False)
