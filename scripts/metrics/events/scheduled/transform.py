import os
import re

import pandas as pd
from lib.util.convert import literal_converter


DATA_DIR=os.path.join('data', 'metrics', 'events', 'master')
os.makedirs(DATA_DIR, exist_ok=True)

ALL_EVENTS=os.path.join(DATA_DIR, 'all.csv')

if __name__ == '__main__':
    from extract import ALL_EVENTS as ALL_EVENTS_RAW
    data = pd.read_csv(ALL_EVENTS_RAW).apply(literal_converter)
    data = data.rename(columns=lambda x: re.sub(r'[\s\-/]+', '_', x.lower().strip()))
    data.start_date = pd.to_datetime(data.start_date)
    data = data[(data.start_date < pd.Timestamp.now()) &
                (data.status == '01 - Greenlit')]

    data.sort_index(axis=1).sort_values(['start_date', 'event_name']).to_csv(ALL_EVENTS, index=False)
