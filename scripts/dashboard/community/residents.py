import pandas as pd

from util.geography import LEEDS_LA_CODE
import dashboard.community.schools

def summarise_activity():
    name_map = pd.read_csv(
        'data/reference/leeds_wards.csv', index_col='WD21CD')

    # Ballot
    ballot = pd.read_csv('data/metrics/ballot/ballot_entries.csv', usecols=[
        'date_submitted', 'ward_code', 'la_code'], parse_dates=['date_submitted']).rename(columns={'date_submitted': 'count'})
    ballot = ballot[ballot['la_code'] == LEEDS_LA_CODE].drop(
        columns=['la_code']).groupby('ward_code').count().reset_index()
    ballot['activity'] = 'ballot'

    volunteers = pd.read_csv('data/metrics/volunteers/volunteers.csv', usecols=[
        'hash', 'ward_code', 'local_authority_code']).rename(columns={'hash': 'count'})
    volunteers = volunteers[volunteers['local_authority_code'] == LEEDS_LA_CODE].drop(
        columns=['local_authority_code']).groupby('ward_code').count().reset_index()
    volunteers['activity'] = 'volunteering'

    roadshow = pd.read_csv('docs/_data/metrics/roadshows/by_ward.csv', usecols=[
                           'ward_code', 'contact_consents']).rename(columns={'contact_consents': 'count'})
    roadshow = roadshow[roadshow.ward_code.isin(name_map.index.values)]
    roadshow['activity'] = 'roadshow_contact'

    schools = dashboard.community.schools.load_schools().drop(
      columns=['total_engagements']
    ).rename(columns={'total_number_of_learners': 'count'})
    schools['activity'] = 'schools_learners'

    # Create report
    report = pd.concat([
        ballot,
        volunteers,
        roadshow,
        schools,
    ]).pivot(columns='activity', index='ward_code').droplevel([0], axis='columns').fillna(0).astype(int)

    # Add a total column
    report['total'] = report.sum(1)

    # Augment the table with the ward name
    report = report.merge(name_map, left_index=True, right_index=True).rename(
        columns={'WD21NM': 'ward_name'}).sort_values(by=['ward_name'])
    report.index.names = ['ward_code']

    # Save to CSV
    report.to_csv('docs/dashboard/community/_data/residents.csv')
