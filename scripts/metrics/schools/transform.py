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
    '''
    These are the available fields in the extracted view:

    Project name
    Event name
    Project type
    Event type
    L23 Creative Team Lead
    Season
    Access Offer
    WeTrack ID
    AirTable ID
    Is this activity part of a Signature project or a series of different activities under the same banner?
    Which ticket booking system is used?
    CLE - Setting
    CLE - Key Stage
    CLE - Subject Area
    CLE - Activity Type
    CLE - School Timing
    L23 Production Lead
    L23 VE Lead
    Event Unique Identifier
    Last Modified
    Post-event evaluation due?
    Divider1
    Divider2
    Divider3
    Divider4
    Last Modified By.id
    Last Modified By.email
    Last Modified By.name
    Start date
    End date
    Venue (dropdown link)
    What is the activity category?
    What time of the day was the activity?
    How do audiences / participants sign up to attend the activity?
    ACTUAL Audience size / number of participants - IN PERSON
    Did you collect any postcode data from audiences / participants?
    Please provide any other narrative information relating to the event / activity
    School
    Does this event need to go on online What's On?
    Who the transport is for
    Toilets
    Food and beverage offer
    Merchandise offer
    Dietary requirements catered for
    Prohibited items list
    Seating / Standing
    Ward (from Venue)
    Venue Name (from Venue)
    Address Line 1 (from Venue)
    Address Line 2 (from Venue)
    Address Line 3 (from Venue)
    Postcode (from Venue)
    Ward (from School)
    School Name (from School)
    School Address Postcode
    Format
    Website / platform for digital presentation
    ACTUAL Audience size / number of participants - ONLINE
    Creative Learning activity category
    What is the activity artform or type of culture?
    Who will be attending/involved?
    If 'participants' are involved had they had input before the day of the activity/event?
    Event Description
    Status
    Target audience numbers
    Single Event or multiple?
    'Other' activity category - Please give details
    Using L23 Ticketing Team?
    "Please provide a narrative description of audiences / participants. This might include: gender, age, ethnicity, disability"
    "If it is repeated, how many times?"
    Notes on Date(s) and Time(s)
    Date Locked
    Did you collect any demographic data from audiences / participants?
    Participation Type
    Age advisory
    In S2 Guide?
    Online launch for 30th March
    Event length
    Venue notes
    Written Credits
    Primary Venue Contact
    CLE Facilitator
    Duty Safeguarding Lead
    Number of booked participants
    Email (from CLE Facilitator)
    Name (from CLE Facilitator)
    Telephone (from CLE Other staff in attendance)
    CLE Facilitator email
    CLE Facilitator Phone
    School Address Line 1
    School Address Line 2
    School Address Line 3
    'Other' artform or type of culture category - Please give details
    Allocated or Unallocated
    Ticket pricing policy
    Start Time
    End Time
    Ticketing notes
    On sale date
    Price A
    Total tickets available
    Target audience profile
    '''
    # Load the file
    data = pd.read_csv(RAW_SCHOOLS_DATA).apply(func=literal_converter)

    # Slugify the column names
    data.rename(columns=lambda x: re.sub(
        r"\W+", '_', x.lower()).strip('_'), inplace=True)

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

    # Save the schools data
    data.to_csv(SCHOOLS_DATA, index=False)

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
        'participant_count': data.actual_audience_size_number_of_participants_in_person,
    }).sort_values('date').query('~date.isna()').query('date < @today')

    events['school_count'] = events.schools.map(len)

    events.to_csv(SCHOOLS_DATA, index=False)
