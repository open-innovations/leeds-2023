import pandas as pd
import os
import yaml

DATA_DIR = os.path.join('data', 'metrics', 'media_coverage')
VIEW_DIR = os.path.join('docs', 'metrics', 'media_coverage', '_data')
os.makedirs(VIEW_DIR, exist_ok=True)

MEDIA_START_DATE = '2021-01-01'
MEDIA_END_DATE = '2023-12-31'

if __name__ == '__main__':
    cision_data = pd.read_csv(os.path.join(
        DATA_DIR, 'combined_cision.csv'), parse_dates=['news_date'])
    historic_data = pd.read_csv(os.path.join(
        DATA_DIR, 'combined_historic.csv'), parse_dates=['news_date'])

    # combine historic
    data = pd.concat([cision_data, historic_data]).sort_values('news_date')
    data = data[data['news_date'].between(MEDIA_START_DATE, MEDIA_END_DATE)]

    # Coverage by Outlet - TODO: rename hsitoric outlets
    outlet_count = pd.DataFrame({'count': data.groupby(['outlet_name'])[
                                'news_headline'].count()}).sort_values('count', ascending=False).head(5)
    outlet_count.to_csv(os.path.join(VIEW_DIR, 'outlet_count.csv'))

    # Coverage by Medium
    data['medium'] = data['medium'].replace(
        {'Newspaper': 'Print', 'Magazine': 'Print', 'Broadcat': 'Broadcast', 'Pdf': 'Online'})
    medium_count = pd.DataFrame({'count': data.groupby(
        ['medium'])['news_headline'].count()}).sort_values('count', ascending=False)
    medium_count.to_csv(os.path.join(VIEW_DIR, 'medium_count.csv'))

    # Break down by date / region
    REGION_TAGS = ['International', 'National', 'Regional', 'Local', 'Unknown']
    by_region = data.filter(['news_date', 'custom_tags', 'news_headline'])
    by_region.news_date = by_region.news_date.dt.to_period('M')
    by_region = by_region.set_index('news_date')
    by_region = by_region.custom_tags \
        .str.split(";").explode() \
        .str.strip() \
        .fillna('Unknown') \
        .to_frame('region')
    by_region = by_region[by_region.region.isin(REGION_TAGS)]
    pre_check = by_region.value_counts().sum()
    by_region['count'] = 1
    by_region = by_region.groupby(['news_date', 'region']) \
        .count().reset_index() \
        .pivot(index="news_date", columns="region", values="count") \
        .fillna(0) \
        .astype(int)
    by_region['Total'] = by_region.sum(axis=1)
    # Check that we got the number out that we were expecting to
    assert (by_region.Total.sum() == pre_check)
    by_region.to_csv(os.path.join(VIEW_DIR, 'monthly_count.csv'))

    # Summary Stats
    uv_max = int(data['uv'].max())
    reach_max = int(data['audience_reach'].max())
    total_audience_reach = int(data.audience_reach.sum())
    total_unique_views = int(data.uv.sum())

    stats = ({
        'total_media': int(data['news_headline'].count()),
        'uv_max': uv_max,
        'uv_max_outlet': data[data['uv'] == uv_max]['outlet_name'].values[0],
        'reach_max': reach_max,
        'reach_max_outlet': data[data['audience_reach'] == reach_max]['outlet_name'].values[0],
        'total_media_local': int(by_region.Local.sum()),
        'total_media_regional': int(by_region.Regional.sum()),
        'total_media_national': int(by_region.National.sum()),
        'total_media_international': int(by_region.International.sum()),
        'total_media_unknown': int(by_region.Unknown.sum()),
        'total_audience_reach': total_audience_reach,
        'total_unique_views': total_unique_views,
        'total_estimated_circulation': total_audience_reach + total_unique_views
    })

    with open(os.path.join(VIEW_DIR, 'stats.yml'), 'w') as f:
        yaml.safe_dump(stats, f)
