import pandas as pd


def summarise_events():
    # Load Roadshows
    roadshows = pd.read_csv('data/metrics/roadshows/attendance.csv', usecols=[
                            'wd21cd', 'date'], parse_dates=['date']).rename(columns={'wd21cd': 'ward_code', 'date': 'events'}).groupby('ward_code').count().reset_index()
    roadshows['event_type'] = 'roadshow'

    # Load MWMCMN Celebration Events
    celebration_event = pd.read_csv('docs/_data/metrics/mwmcmn/celeb_event_by_ward.csv',
                                    usecols=['ward_code', 'celeb_events']).rename(columns={'celeb_events': 'events'})
    celebration_event['event_type'] = 'celebration_event'

    schools = pd.read_csv('data/metrics/schools/schools_engagement.csv').drop(
        columns=['total_number_of_learners']
    ).rename(columns={'total_engagements': 'events'})
    schools['event_type'] = 'schools_engagement'

    report = pd.concat([
        roadshows,
        celebration_event,
        schools,
    ]).pivot(columns='event_type', index='ward_code').droplevel([0], axis='columns').fillna(0).astype(int)

    report['ward_hosts'] = 1

    report['total'] = report.sum(1)

    name_map = pd.read_csv(
        'data/reference/leeds_wards.csv', index_col='WD21CD')
    report = report.merge(name_map, left_index=True, right_index=True).rename(
        columns={'WD21NM': 'ward_name'}).sort_values(by=['ward_name'])
    report.index.names = ['ward_code']

    report.to_csv('docs/dashboard/community/_data/events.csv')


if __name__ == '__main__':
    summarise_events()
