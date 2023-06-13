import os
import re

import pandas as pd
from lib.util.convert import literal_converter

from extract import ALL_EVENTS as ALL_EVENTS_RAW

DATA_DIR=os.path.join('data', 'metrics', 'events', 'master')
os.makedirs(DATA_DIR, exist_ok=True)

ALL_EVENTS=os.path.join(DATA_DIR, 'all.csv')

if __name__ == '__main__':
    data = pd.read_csv(ALL_EVENTS_RAW).apply(literal_converter)
    data = data.rename(columns=lambda x: re.sub(r'[\s\-/]+', '_', x.lower().strip()))

    data.to_csv(ALL_EVENTS, index=False)
