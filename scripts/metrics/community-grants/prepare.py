import os
import pandas as pd

from transform import RESPONSE_CSV

SITE_DIR = os.path.join('docs', 'metrics', 'community-grants', '_data')
os.makedirs(SITE_DIR, exist_ok=True)

if __name__ == '__main__':
    responses = pd.read_csv(RESPONSE_CSV, parse_dates=['date_submitted'])

    responses_by_la = pd.DataFrame({
        'responses': responses.groupby(['la_code']).date_submitted.count(),
    }).fillna(0).astype(int)
    responses_by_la.sort_values(by=['la_code']).to_csv(os.path.join(
        SITE_DIR, 'responses_by_la.csv'))

    responses_by_ward = pd.DataFrame({
        'responses': responses.groupby(['ward_code']).date_submitted.count(),
    }).fillna(0).astype(int)
    responses_by_ward.sort_values(by=['ward_code']).to_csv(os.path.join(
        SITE_DIR, 'responses_by_ward.csv'))

    responses_by_week = pd.DataFrame({
        'responses': responses.groupby(['date_submitted']).ward_code.count(),
    }).fillna(0).resample('W-FRI').sum().astype(int)
    responses_by_week.to_csv(os.path.join(SITE_DIR, 'responses_by_week.csv'))

    summary = responses_by_week.sum()
    summary.to_json(os.path.join(SITE_DIR, 'headline.json'))
