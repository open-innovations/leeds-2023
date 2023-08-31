import pandas as pd

from util.geography import LEEDS_LA_CODE


def get_event_awakening():
    data = pd.read_csv('data/metrics/events/awakening/attendees.csv', usecols=[
        'ward_code', 'la_code', 'awakening_attended'
    ]).rename(columns={'awakening_attended': 'count'})
    data = data[data.la_code == LEEDS_LA_CODE].drop(
        columns='la_code').groupby('ward_code').sum().reset_index()
    data['activity'] = 'awakening_attendance'
    return data

def get_event_the_barn():
    data = pd.read_csv('docs/metrics/events/the-barn/_data/events/by_ward.csv', usecols=[
        'ward_code', 'audience'
    ]).rename(columns={'audience': 'count'})
    data['activity'] = 'the_barn_residents'
    return data

def get_signature_events(): 
    data = pd.read_csv('docs/metrics/events/signature/_data/tickets_by_ward.csv', usecols=[
        'ward_code', 'tickets'
    ]).rename(columns={'tickets': 'count'})
    data['activity'] = 'signature_events'
    return data



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

    roadshow = pd.read_csv('docs/metrics/roadshow-attendees/_data/by_ward.csv', usecols=[
                           'ward_code', 'contact_consents']).rename(columns={'contact_consents': 'count'})
    roadshow = roadshow[roadshow.ward_code.isin(name_map.index.values)]
    roadshow['activity'] = 'roadshow_contact'

    schools = pd.read_csv('docs/metrics/schools/_data/engagements_by_ward.csv')[['ward_code', 'pupil_engagements']].rename(columns={'pupil_engagements': 'count'})
    schools['activity'] = 'schools_learners'

    awakening = get_event_awakening()

    the_barn = get_event_the_barn()

    signature_events = get_signature_events()

    # Create report
    report = pd.concat([
        ballot,
        awakening,
        the_barn,
        signature_events,
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
    report.to_csv('docs/dashboard/community/_data/residents_with_schools.csv')

    # Create version without schools data
    report.drop(columns=['schools_learners', 'total'], inplace=True)
    report['total'] = report.sum(1, numeric_only=True)
    report.to_csv('docs/dashboard/community/_data/residents.csv')


if __name__ == '__main__':
    summarise_activity()
