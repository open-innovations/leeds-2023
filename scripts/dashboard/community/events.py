import pandas as pd

def load_data(path, id, **kwargs):
    data = pd.read_csv(path, **kwargs)
    data['event_type'] = id
    return data


def summarise_events():
    # Load Roadshows
    roadshows = pd.read_csv('data/metrics/roadshows/attendance.csv', usecols=[
                            'wd21cd', 'date'], parse_dates=['date']).rename(columns={'wd21cd': 'ward_code', 'date': 'events'}).groupby('ward_code').count().reset_index()
    roadshows['event_type'] = 'roadshow'

    # The rest of these are already summarised by ward, can just load and remap
    celebration_event = load_data('docs/_data/metrics/mwmcmn/celeb_event_by_ward.csv', 'celebration_event', usecols=['ward_code', 'celeb_events']).rename(columns={'celeb_events': 'events'})
    schools = load_data('docs/metrics/schools/_data/engagements_by_ward.csv', 'schools_engagement', usecols=['ward_code', 'total_engagements']).rename(columns={'total_engagements': 'events'})
    hidden_stories = load_data('docs/_data/metrics/hidden_stories/wards.csv','hidden_stories', usecols=['ward_code','count']).rename(columns={'count':'events'})
    my_leeds = load_data('docs/metrics/events/my-leeds-2023/_data/events/by_ward.csv', 'my_leeds_2023', usecols=['ward_code','events'])
    the_barn = load_data('docs/metrics/events/the-barn/_data/events/by_ward.csv', 'the_barn', usecols=['ward_code','events'])
    signature = load_data('docs/metrics/events/signature/_data/events_by_ward.csv', 'signature', usecols=['ward_code','events'])
    partner = load_data('docs/metrics/events/partner/_data/by_ward.csv', 'partner', usecols=['ward_code','events'])

    #Combine
    report = pd.concat([
        my_leeds,
        the_barn,
        signature,
        partner,
        roadshows,
        celebration_event,
        schools,
        hidden_stories
    ]).pivot(columns='event_type', index='ward_code').droplevel([0], axis='columns').fillna(0).astype(int)

    report['ward_hosts'] = 1

    report['total'] = report.sum(1)

    name_map = pd.read_csv(
        'data/reference/leeds_wards.csv', index_col='WD21CD')

    report = report.merge(name_map, left_index=True, right_index=True).rename(
        columns={'WD21NM': 'ward_name'}).sort_values(by=['ward_name'])
    report.index.names = ['ward_code']

    report.to_csv('docs/dashboard/community/_data/events_with_schools.csv')

    # Remove schools data
    report.drop(columns=['schools_engagement', 'total'], inplace=True)
    report['total'] = report.sum(1, numeric_only=True)
    report.to_csv('docs/dashboard/community/_data/events.csv')


if __name__ == '__main__':
    summarise_events()
