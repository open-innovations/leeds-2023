import os
import pandas as pd

from transform import RESPONSE_CSV

SITE_DIR = os.path.join('docs', 'metrics', 'events', 'my-leeds-2023', '_data')
os.makedirs(SITE_DIR, exist_ok=True)

if __name__ == '__main__':
    responses = pd.read_csv(RESPONSE_CSV, parse_dates=['date_submitted'])

    responses_by_la = pd.DataFrame({
        'responses': responses.groupby(['la_code', 'grant']).date_submitted.count(),
    }).reset_index().pivot(index='la_code', columns='grant', values='responses').fillna(0).astype(int)
    responses_by_la['total_responses'] = responses_by_la.sum(1)
    responses_by_la.sort_values(by=['la_code']).to_csv(os.path.join(
        SITE_DIR, 'responses_by_la.csv'))

    responses_by_ward = pd.DataFrame({
        'responses': responses.groupby(['ward_code', 'grant']).date_submitted.count(),
    }).reset_index().pivot(index='ward_code', columns='grant', values='responses').fillna(0).astype(int)
    responses_by_ward['total_responses'] = responses_by_ward.sum(1)
    responses_by_ward.sort_values(by=['ward_code']).to_csv(os.path.join(
        SITE_DIR, 'responses_by_ward.csv'))

    responses_by_week = pd.DataFrame({
        'responses': responses.groupby(['date_submitted', 'grant']).ward_code.count(),
    }).reset_index().pivot(index='date_submitted', columns='grant', values='responses').fillna(0).resample('W-FRI').sum().astype(int)
    responses_by_week['total_responses'] = responses_by_week.sum(1)
    responses_by_week.to_csv(os.path.join(SITE_DIR, 'responses_by_week.csv'))

    summary = responses_by_week.sum()
    summary['unknown_ward'] = responses[responses.ward_code == 'UNKNOWN'].date_submitted.count()
    summary.to_json(os.path.join(SITE_DIR, 'headline.json'))
