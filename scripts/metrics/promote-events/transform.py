import os
import re
import pandas as pd
from extract import EVENTS_SOURCE_DATA
import util.geography as geo

DATA_DIR = 'data/metrics/events/promote-events/'
EVENTS_DATA = os.path.join(DATA_DIR, 'events.csv')

columns = {
  'Event Name': 'name',
  'Event Start Date': 'start_date',
  'Event End Date': 'end_date',
  'Venue - including address': 'venue',
  'Stage': 'stage',
  'Live date': 'status',
}


if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)

    data = pd.read_csv(EVENTS_SOURCE_DATA)

    # Reshape data
    data = data[columns.keys()].rename(columns=columns)
    data.start_date = pd.to_datetime(data.start_date)
    data.end_date = pd.to_datetime(data.end_date)
    
    # Ward mapping
    postcode = data.venue.str.extract(r'(?P<postcode>LS\d+\s+\d[A-Z]{2})', flags=re.IGNORECASE).postcode.apply(geo.postcode_formatter)
    data['ward_code'] = postcode.map(geo.postcode_to_ward_code)
    
    data.drop(columns=['venue'], inplace=True)

    data[data.name.notna()].to_csv(EVENTS_DATA, index=False)