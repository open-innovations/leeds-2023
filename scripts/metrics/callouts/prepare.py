import os
import pandas as pd

from metrics.callouts.transform import RESPONSE_CSV

SITE_DIR = os.path.join('docs', 'metrics', 'callouts', '_data')
os.makedirs(SITE_DIR, exist_ok=True)

if __name__ == '__main__':
    responses = pd.read_csv(RESPONSE_CSV)

    responses_by_callout = pd.DataFrame({
        'responses': responses.groupby(['callout']).date_submitted.count()
    })
    responses_by_callout.sort_values(by=['callout']).to_csv(os.path.join(
        SITE_DIR, 'responses_by_callout.csv'))

    responses_by_la = pd.DataFrame({
        'responses': responses.groupby(['la_code']).date_submitted.count(),
    })
    responses_by_la.sort_values(by=['la_code']).to_csv(os.path.join(
        SITE_DIR, 'responses_by_la.csv'))

    responses_by_ward = pd.DataFrame({
        'responses': responses.groupby(['ward_code']).date_submitted.count(),
    })
    responses_by_ward.sort_values(by=['ward_code']).to_csv(os.path.join(
        SITE_DIR, 'responses_by_ward.csv'))

    summary = responses_by_callout.sum()
    summary.to_json(os.path.join(SITE_DIR, 'headline.json'))
