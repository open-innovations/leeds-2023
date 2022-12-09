import pandas as pd
import json
import os

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

#Merge to get local authority code
with open(os.path.join('working','arts_council','la.json')) as f:
    hex_data = pd.DataFrame.from_dict(json.load(f)['hexes'],orient='index')

hex_data['la_code'] = hex_data.index

combined = (pd.merge(hex_data,by_la,left_on='n',right_index=True,how='left')
              .rename(columns={'n':'local_authority'}).drop(columns=['q','r','region','lad19nmw','colour']))


#Merge with population stats
PS_PATH = os.path.join('working','arts_council','ukpopestimatesmid2020on2021geography.xlsx')
population_stats = pd.read_excel(PS_PATH,skiprows=7,usecols=['Code','Name','Geography','All ages'])


combined = (pd.merge(combined,population_stats,left_on='la_code',right_on='Code',how='inner')
               .drop(columns=['Name','Code','Geography'])
               .rename(columns={'All ages' : 'population'})
               .sort_values('la_code'))

combined['sum_total_per_capita'] = ((combined['sum_total'] / combined['population']).round(2)).fillna(0).map('{:,.2f}'.format).replace({'0.00':'0'})
combined = combined[['la_code','local_authority','population','count_total','sum_total','sum_total_per_capita']]
combined.to_csv(os.path.join('docs','_data','arts_council','all_summary_hex.csv'),index=False)
