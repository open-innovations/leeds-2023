import pandas as pd
import os
import yaml

DATA_DIR = os.path.join('data','metrics','media_coverage')
VIEW_DIR = os.path.join('docs','_data','metrics','media_coverage','summary_new')


cision_data = pd.read_csv(os.path.join(DATA_DIR,'combined_cision.csv'),parse_dates=['news_date'])
historic_data = pd.read_csv(os.path.join(DATA_DIR,'combined_historic.csv'),parse_dates=['news_date'])

data = pd.concat([cision_data,historic_data]).sort_values('news_date')

data = data[data['news_date'].between('2021-01-01','2022-12-31')]


outlet_count = pd.DataFrame({'count' : data.groupby(['outlet_name'])['news_headline'].count()}).sort_values('count',ascending=False).head(5)
outlet_count.to_csv(os.path.join(VIEW_DIR,'outlet_count.csv'))

data['medium'] = data['medium'].replace({'Newspaper' : 'Print', 'Magazine' : 'Print','Broadcat' : 'Broadcast', 'Pdf' : 'Online'})
medium_count = pd.DataFrame({'count' : data.groupby(['medium'])['news_headline'].count()}).sort_values('count',ascending=False)
medium_count.to_csv(os.path.join(VIEW_DIR,'medium_count.csv'))

data['month'] = data['news_date'].dt.to_period('M')
month_count = pd.DataFrame({'count' : data.groupby(['month'])['news_headline'].count()})
month_count.to_csv(os.path.join(VIEW_DIR,'monthly_count.csv'))

data['custom_tags'] = data['custom_tags'].str.title()
region_tags = ['International','National','Regional','Local']
regional_count = pd.DataFrame({'count' : data[data['custom_tags'].isin(region_tags)].groupby(['custom_tags'])['news_headline'].count()}).sort_values('count')
regional_count.to_csv(os.path.join(VIEW_DIR,'regional_count.csv'))

uv_max = int(data['uv'].max())
reach_max = int(data['audience_reach'].max())
stats = ({
    'total_media' : int(data['news_headline'].count()),
    'uv_max' : uv_max,
    'uv_max_outlet' : data[data['uv'] == uv_max]['outlet_name'].values[0],
    'reach_max' : reach_max,
    'reach_max_outlet' : data[data['audience_reach'] == reach_max]['outlet_name'].values[0],
    'total_media_international' : int(data[data['custom_tags'] == 'International']['news_headline'].count())})

with open(os.path.join(VIEW_DIR,'stats.yml'),'w') as f:
    yaml.safe_dump(stats,f)


