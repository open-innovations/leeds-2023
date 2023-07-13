import os
import pandas as pd

from transform import EVENTS_DATA


SITE_DATA_DIR = os.path.join('docs', 'metrics', 'events', 'partner', '_data')


if __name__ == '__main__':
    os.makedirs(SITE_DATA_DIR, exist_ok=True)
    data = pd.read_csv(EVENTS_DATA, parse_dates=['start_date']).rename(columns={ 'name': 'events' })

    # summary = data[['events']].to_json(, orient='records')
    # os.path.join(SITE_DATA_DIR, 'headline.json')

    by_ward = data.fillna('UNKNOWN').groupby('ward_code').events.count()
    by_ward.to_csv(os.path.join(SITE_DATA_DIR, 'by_ward.csv'))

    by_month = data.groupby('start_date').events.count().resample('M').sum().to_frame()
    by_month['cumulative_events'] = by_month.events.cumsum()
    by_month.to_csv(os.path.join(SITE_DATA_DIR, 'by_month.csv'))

    summary = by_month.reset_index()[['start_date', 'cumulative_events']]
    summary.columns = ['latest_month', 'total_events']
    print(summary)
    summary.iloc[-1].to_json(os.path.join(SITE_DATA_DIR, 'headline.json'), indent=2, date_format='iso')
