import pandas as pd
import json
import os
import yaml

YEARS = ['2018-19_0','2019-20_0','2020-21_0','2021-22_0','2022-23']
WORKING_DIR = os.path.join('working','arts_council')
RAW_FILE_TEMP = 'National Lottery Project Grants - List of awards in year {}.xlsx'
SHEET_NAME = 'Project Grants Awards'

def get_summarys_all():
    summarys = []
    for year in YEARS:
        data = pd.read_excel(os.path.join(WORKING_DIR,RAW_FILE_TEMP.format(year)),sheet_name=SHEET_NAME,skiprows=2,usecols=['Local authority','Award amount'])
        
        summarys.append(data)
    return pd.concat(summarys)

    
data = get_summarys_all()

#replace northamptonshire la values
data['Local authority'] = data['Local authority'].replace({
            'Corby' : 'North Northamptonshire',
            'East Northamptonshire' : 'North Northamptonshire',
            'Kettering' : 'North Northamptonshire' ,
            'Wellingborough' : 'North Northamptonshire',
            'Northampton' : 'West Northamptonshire',
            'South Northamptonshire' : 'West Northamptonshire',
            'Daventry' : 'West Northamptonshire'
        })

by_la = pd.DataFrame({
    'count_total' : data.groupby('Local authority')['Award amount'].count().astype('Int64'),
    'sum_total' : data.groupby('Local authority')['Award amount'].sum().astype('Int64')
})

#Merge to get local and region authority code
with open(os.path.join('working','arts_council','la.json')) as f:
    hex_data = pd.DataFrame.from_dict(json.load(f)['hexes'],orient='index')

hex_data['la_code'] = hex_data.index

combined_la = (pd.merge(hex_data,by_la,left_on='n',right_index=True,how='left')
              .rename(columns={'n':'local_authority'}).drop(columns=['q','r','lad19nmw','colour']))

combined_region = pd.DataFrame({
    'count_total' : combined_la.groupby('region')['count_total'].sum().astype('Int64'),
    'sum_total' : combined_la.groupby('region')['sum_total'].sum().astype('Int64')
})

#Merge with population stats
PS_PATH = os.path.join('working','arts_council','ukpopestimatesmid2020on2021geography.xlsx')
population_stats = pd.read_excel(PS_PATH,skiprows=7,usecols=['Code','Name','Geography','All ages'],index_col='Code')

combined_la = (pd.merge(combined_la,population_stats,left_on='la_code',right_index=True,how='inner')
               .drop(columns=['Name','Geography'])
               .rename(columns={'All ages' : 'population'})
               .sort_values('la_code'))


combined_region = (pd.merge(combined_region,population_stats,left_index=True,right_index=True,how='inner')
               .drop(columns=['Geography'])
               .rename(columns={'All ages' : 'population','Name' : 'region'})
               .rename_axis('region_code')
               .sort_index())

          

combined_la['sum_total_per_capita'] = ((combined_la['sum_total'] / combined_la['population']).round(2)).fillna(0).map('{:,.2f}'.format).replace({'0.00':'0'})
combined_la = combined_la[['la_code','local_authority','population','count_total','sum_total','sum_total_per_capita']]
combined_la.to_csv(os.path.join('docs','_data','arts_council','all_summary_hex.csv'),index=False)


combined_region['sum_total_per_capita'] = ((combined_region['sum_total'] / combined_region['population']).round(2)).fillna(0).map('{:,.2f}'.format).replace({'0.00':'0'})
combined_region = combined_region[['region','population','count_total','sum_total','sum_total_per_capita']]
combined_region.to_csv(os.path.join('docs','_data','arts_council','all_summary_region.csv'))

#yaml region file
combined_region['sum_total_per_capita_f'] = (combined_region['sum_total'] / combined_region['population']).round(2)
combined_region.index = combined_region['region'].str.title()

out_region = combined_region[['sum_total_per_capita_f']].to_dict()['sum_total_per_capita_f']
print(out_region)
with open(os.path.join('docs','_data','arts_council','region_map.yaml'),'w') as f:
    yaml.safe_dump(out_region,f)


uk_pop = population_stats[population_stats['Name'] == 'UNITED KINGDOM']['All ages'][0]
england_pop = population_stats[population_stats['Name'] == 'ENGLAND']['All ages'][0]
stats = {
    'total_count' : data['Award amount'].count(),
    'total_sum' : data['Award amount'].sum(), 
    'uk_count' : combined_region['count_total'].sum(),
    'uk_sum' : combined_region['sum_total'].sum(),
    'england_count' : combined_region[~combined_region['region'].isin(['NORTHERN IRELAND','SCOTLAND','WALES'])]['count_total'].sum(),
    'england_sum' : combined_region[~combined_region['region'].isin(['NORTHERN IRELAND','SCOTLAND','WALES'])]['sum_total'].sum(),
    'uk_population' : uk_pop,
    'england_population' : england_pop
}

for s in stats.keys():
    stats[s] = int(stats[s])

print(stats)
with open(os.path.join('docs','_data','arts_council','stats.yaml'),'w') as f:
    yaml.safe_dump(stats,f)
