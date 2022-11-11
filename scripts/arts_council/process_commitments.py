import pandas as pd
import os

RAW_DIR = 'working\\arts_council'
GRANTS_Q1 = 'Grant_commitments_2022-23_Qtr1.xlsx'

in_path = os.path.join(RAW_DIR,GRANTS_Q1)

data = pd.read_excel(in_path,skiprows=6,usecols='A:K')
ward_names = pd.read_csv('working\\arts_council\\wards-leeds.csv')

data = data.loc[data['Local Authority'] == 'Leeds']

processed = pd.DataFrame({
   'count' : data.groupby(' Ward')[' Ward'].count(),
   'amount' : data.groupby(' Ward')['Grant Amount'].sum()
}).reset_index().rename(columns={' Ward' : 'name'})
processed['name'] = processed['name'].str.replace('&','and')
processed = pd.merge(processed,ward_names,on='name',how='right').fillna(0)
processed.to_csv('testing_ac_2.csv',index=False)

