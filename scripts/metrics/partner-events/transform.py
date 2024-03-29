import ast
import os
import re
import pandas as pd
from extract import EVENTS_SOURCE_DATA
import scripts.util.geography as geo


DATA_DIR = 'data/metrics/events/partner-events/'
EVENTS_DATA = os.path.join(DATA_DIR, 'events.csv')

columns = {
    'Event Name': 'name',
    'Event Start Date': 'start_date',
    'Event End Date': 'end_date',
    'Ward': 'ward',
    'Venue - including address': 'venue',
    'Venue postcode': 'postcode',
    'Pricing Policy': 'pricing',
    'Live date': 'live_date',
    'Partner/Promote': 'partner_promote',
    'Is this event on Leeds Inspried?': 'on_leeds_inspired',
    'Key Event Partner': 'key_partner',
}


def literal_converter(series):
    def convert(value):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value
    return series.apply(convert)


if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)

    data = pd.read_csv(EVENTS_SOURCE_DATA).apply(literal_converter)

    # Reshape data
    data = data[
        data.columns.intersection(columns.keys(), sort=False)
    ].rename(columns=columns)
    data.start_date = pd.to_datetime(data.start_date)
    data.end_date = pd.to_datetime(data.end_date)
    data = data.explode('ward')

    # Ward mapping
    data['ward_name'] = data.ward.apply(geo.normalise_leeds_ward)
    data['ward_code'] = data.ward.map(geo.leeds_ward_name_to_code)

    data.drop(columns=['ward', 'ward_name'], inplace=True)

    data[data.name.notna()].to_csv(EVENTS_DATA, index=False)
