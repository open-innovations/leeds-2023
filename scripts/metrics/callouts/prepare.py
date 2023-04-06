import os
import pandas as pd

from metrics.callouts.transform import RESPONSE_CSV

SITE_DIR = os.path.join('docs', 'metrics', 'callouts', '_data')
os.makedirs(SITE_DIR, exist_ok=True)

if __name__ == '__main__':
    responses = pd.read_csv(RESPONSE_CSV, parse_dates=['date_submitted'])

    responses_by_callout = pd.DataFrame({
        'responses': responses.groupby(['callout']).date_submitted.count()
    })
    responses_by_callout.sort_values(by=['callout']).to_csv(os.path.join(
        SITE_DIR, 'responses_by_callout.csv'))

    responses_by_la = pd.DataFrame({
        'responses': responses.groupby(['la_code', 'callout']).date_submitted.count(),
    }).reset_index() \
      .pivot(index='la_code', columns='callout', values='responses') \
      .fillna(0).astype(int)
    responses_by_la['responses'] = responses_by_la.sum(axis=1)
    responses_by_la['barn_plus_wow_responses'] = responses_by_la.become_a_barn_raiser + responses_by_la.become_a_wowser
    responses_by_la.sort_values(by=['la_code']).to_csv(os.path.join(
        SITE_DIR, 'responses_by_la.csv'))

    responses_by_ward = pd.DataFrame({
        'responses': responses.groupby(['ward_code', 'callout']).date_submitted.count(),
    }).reset_index() \
      .pivot(index='ward_code', columns='callout', values='responses') \
      .fillna(0).astype(int)
    responses_by_ward['responses'] = responses_by_ward.sum(axis=1)
    responses_by_ward['barn_plus_wow_responses'] = responses_by_ward.become_a_barn_raiser + responses_by_ward.become_a_wowser
    responses_by_ward.sort_values(by=['ward_code']).to_csv(os.path.join(
        SITE_DIR, 'responses_by_ward.csv'))

    responses_by_week = pd.DataFrame({
        'responses': responses.groupby(['date_submitted', 'callout']).ward_code.count(),
    }).reset_index().pivot(
        index='date_submitted', columns='callout', values='responses'
    ).fillna(0).resample('W-FRI').sum().astype(int)
    responses_by_week.to_csv(os.path.join(SITE_DIR, 'responses_by_week.csv'))

    summary = responses_by_callout.sum()
    summary.to_json(os.path.join(SITE_DIR, 'headline.json'))
