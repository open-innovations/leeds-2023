import os
import pandas as pd

from transform import EVENTS_DATA


SITE_DATA_DIR = os.path.join('docs', 'metrics', 'events', 'partner', '_data')


if __name__ == '__main__':
    os.makedirs(SITE_DATA_DIR, exist_ok=True)
    data = pd.read_csv(EVENTS_DATA, parse_dates=['start_date']).rename(columns={ 'name': 'events' })

    summary = data[['events']].to_json(os.path.join(SITE_DATA_DIR, 'headline.json'))

    data.fillna('UNKNOWN').groupby('ward_code').events.count().to_csv(os.path.join(SITE_DATA_DIR, 'by_ward.csv'))
    data.groupby('start_date').events.count().resample('MS').sum().to_csv(os.path.join(SITE_DATA_DIR, 'by_month.csv'))
