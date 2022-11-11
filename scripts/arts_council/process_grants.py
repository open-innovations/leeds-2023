import pandas as pd

YEARS = ['2018-19_0','2019-20_0','2020-21_0','2021-22_0','2022-23']
RAW_FILE_TEMP = 'working\\arts_council\\National Lottery Project Grants - List of awards in year {}.xlsx'
SHEET_NAME = 'Project Grants Awards'

def get_summarys():
    summarys = []
    for year in YEARS:
        data = pd.read_excel(RAW_FILE_TEMP.format(year),sheet_name=SHEET_NAME,skiprows=2)
        wy_data = data.loc[data['Local authority'].isin(['Leeds','Bradford','Wakefield','Calderdale','Kirklees'])]

        total_count = data['Award amount'].count()
        total_sum = data['Award amount'].sum()

        summary = pd.concat([
        
        pd.DataFrame({
            'count' : wy_data.groupby('Local authority')['Award amount'].count(),
            'sum'   : wy_data.groupby('Local authority')['Award amount'].sum()
        }),

        pd.DataFrame({
            'count' : [wy_data['Award amount'].count(),total_count],
            'sum'   : [wy_data['Award amount'].sum(),total_sum]
        },index=['West_Yorkshire','Total'])
        ])

        summary.index.name = 'Local Authority'

        summary['count_per'] = (100 * (summary['count'] / total_count)).round(2)
        summary['sum_per'] = (100 * (summary['sum'] / total_sum)).round(2)
        summary['year'] = year[:7]
        summarys.append(summary)
    return summarys

data = pd.concat(get_summarys())
#data['Local Authority'] = data.index
data= (  data
        .reset_index()
        .pivot(columns='Local Authority',index='year')
)

data.columns = ['_'.join(col).strip() for col in data.columns.values]
data = data.filter(['count_Leeds','count_per_Leeds','count_West_Yorkshire','count_per_West_Yorkshire','count_Total','sum_Leeds','sum_per_Leeds','sum_West_Yorkshire','sum_per_West_Yorkshire','sum_Total'])
data.to_csv('docs\\_data\\metrics\\arts_council\\leeds_summary.csv')
print(data)
    


