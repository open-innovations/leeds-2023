import os
import pandas as pd

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


def read_tracker():
    data = pd.read_excel(
        'working/manual/schools/School Engagement Tracker.xlsx',
        sheet_name='Sheet1',
        usecols="A:C"
    )
    data.columns = [
        'school_name',
        'ward',
        'sector'
    ]
    data = data[data.school_name.notna()]
    return data


if __name__ == '__main__':
    data = read_tracker()
    data = clean_schoolnames(data)
    data = clean_wardnames(data)
    extra_schools = pd.read_csv(os.path.join(os.path.dirname(__file__), 'schools_to_add.csv'))
    data = pd.concat([data, extra_schools], ignore_index=True)

    data.to_csv('data/reference/schools.csv', index=False)