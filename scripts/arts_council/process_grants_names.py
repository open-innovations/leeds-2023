import pandas as pd

YEARS = ['2018-19_0','2019-20_0','2020-21_0','2021-22_0','2022-23']
RAW_FILE_TEMP = 'working\\arts_council\\National Lottery Project Grants - List of awards in year {}.xlsx'
SHEET_NAME = 'Project Grants Awards'

def get_top_recipients(x,local_as=None):
    summarys = []
    for year in YEARS:
        data = pd.read_excel(RAW_FILE_TEMP.format(year),sheet_name=SHEET_NAME,skiprows=2)
        la_data = data.loc[:,['Recipient','Activity name','Award amount','Award date','Local authority']]
        
        if local_as is not None:
            la_data = la_data.loc[la_data['Local authority'].isin(local_as)]

        summarys.append(la_data)
    df =  pd.concat(summarys).sort_values('Award amount',ascending=False).head(x)
    df['Award amount'] = '£'+ df['Award amount'].map('{:,.0f}'.format)
    return df

get_top_recipients(25,['Leeds']).to_csv('docs\\_data\\metrics\\arts_council\\leeds_recipients.csv',index=False)
get_top_recipients(25,['Leeds','Bradford','Wakefield','Calderdale','Kirklees']).to_csv('docs\\_data\\metrics\\arts_council\\wy_recipients.csv',index=False)
get_top_recipients(25).to_csv('docs\\_data\\metrics\\arts_council\\national_recipients.csv',index=False)


    


