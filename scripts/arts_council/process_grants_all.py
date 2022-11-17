import pandas as pd
import json

YEARS = ['2018-19_0','2019-20_0','2020-21_0','2021-22_0','2022-23']
RAW_FILE_TEMP = 'working\\arts_council\\National Lottery Project Grants - List of awards in year {}.xlsx'
SHEET_NAME = 'Project Grants Awards'

def get_summarys_all():
    summarys = []
    for year in YEARS:
        data = pd.read_excel(RAW_FILE_TEMP.format(year),sheet_name=SHEET_NAME,skiprows=2)
        
        total_count = data['Award amount'].count()
        total_sum = data['Award amount'].sum()

        summary = pd.DataFrame({
            'count' : data.groupby('Local authority')['Award amount'].count(),
            'sum'   : data.groupby('Local authority')['Award amount'].sum()
        })

        summary.index.name = 'Local Authority'

        #summary['count_per'] = (100 * (summary['count'] / total_count)).round(2)
        #summary['sum_per'] = (100 * (summary['sum'] / total_sum)).round(2)
        summary['year'] = year[:7]
        summarys.append(summary)
    return summarys

    
data = pd.concat(get_summarys_all())
data=  data.pivot(columns='year')


data.columns = ['_'.join(col).strip() for col in data.columns.values]
data.to_csv('docs\\_data\\metrics\\arts_council\\all_summary.csv')

data['las'] = data.index
with open('working\\arts_council\\la.json') as f:
    hex_data = pd.DataFrame.from_dict(json.load(f)['hexes'],orient='index')

combined = pd.merge(hex_data,data,left_on='n',right_on='Local Authority',how='left')
combined.pop('region')
combined = combined.rename(columns={'n':'id'})

for col in ['count_2018-19','count_2019-20','count_2020-21','count_2021-22','count_2022-23','sum_2018-19','sum_2019-20','sum_2020-21','sum_2021-22','sum_2022-23']:
    combined[col] = combined[col].astype('Int64')
    combined[col] = combined[col].fillna(0)

combined.to_csv('docs\\_data\\metrics\\arts_council\\all_summary_hex.csv',index=False)
print(combined)