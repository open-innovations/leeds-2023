import pandas as pd
import os

RAW_DATA_DIR = os.path.join('working','manual','media') 
HISTORIC_PATH = os.path.join(RAW_DATA_DIR,'Leeds 2023 AVE.xlsx')
CISION_PATH = os.path.join(RAW_DATA_DIR,'Cision - Leeds 2023 23 Sept - 17 Oct for OI.csv') 
OUTPUT_PATH = os.path.join('data','metrics','media_coverage','combined_historic.csv')

historic_columns = ['Outlet Name','News Headline','News Date','Type','Messaging','Tone','Custom Tags','Tier','Medium','Audience Reach']
historic_data = pd.read_excel(HISTORIC_PATH,usecols='A:J',nrows=335,sheet_name='Aug 2021 - July 2022',names=historic_columns,parse_dates=['News Date'])
historic_data['News Date'] = historic_data['News Date'].replace(['November','3.22','8.4.22','29.5.22'],['01.11.21','01.03.22','08.04.22','29.05.22'])
historic_data['News Date'] = pd.to_datetime(historic_data['News Date'],dayfirst=True)
historic_data['Tone'] = historic_data['Tone'].replace({'\s*Positive\s*' : 'POS','\s*Negative\s*' : 'NEG','\s*Neutral\s*' : 'NEU'},regex=True)

historic_columns_2 = ['Tier','Outlet Name','News Date','News Headline','Type','Custom Tags','Medium','Audience Reach']
historic_data_2 = pd.read_excel(HISTORIC_PATH,usecols='A:H',nrows=217,sheet_name='April 2020-July 2021',names=historic_columns_2,parse_dates=['News Date'])
historic_data_2['News Date'] = historic_data_2['News Date'].replace(['20.02.02','1/14/1900'],['20.02.20','14.05.21'])
historic_data_2['Medium'] = historic_data_2['Medium'].str.capitalize()

#Fill in missing Dates
historic_data_2.at[54,'News Date'] = '03.03.21'
historic_data_2.at[55,'News Date'] = '03.03.21'
historic_data_2.at[95,'News Date'] = '25.05.21'
historic_data_2.at[142,'News Date'] = '07.08.21'
historic_data_2.at[143,'News Date'] = '07.08.21'

historic_data_2['News Date'] = pd.to_datetime(historic_data_2['News Date'],dayfirst=True)


#cision_data = pd.read_csv(CISION_PATH,parse_dates=['News Date'],dayfirst=True)

columns_order = ['News Date','News Headline','Outlet Name','Audience Reach','Tone','Medium','Custom Tags']

# Drop columns and sort by date
combined_data = (pd.concat([historic_data,historic_data_2])
                    .drop(columns=['Tier','Type','Messaging',])
                    .sort_values(by=['News Date','News Headline','Medium'])
                    .reindex(columns=columns_order)
                )

#change column types 
combined_data['Audience Reach'] = combined_data['Audience Reach'].astype('string').str.replace(',|\s|\.0|N/A','',regex=True).replace('',None).astype('Int64')
#combined_data['UV*'] = combined_data['UV*'].astype('Int64')

#change column names
combined_data.columns = combined_data.columns.str.replace(' ','_').str.replace('*','',regex=False).str.lower()

#strip string columns
df_obj = combined_data.select_dtypes(['object'])
combined_data[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

""""
#Rename outlets to cision name if found
combined_data['outlet_name'] = combined_data['outlet_name'].replace({
  'Yorkshire evening post' : 'Yorkshire Evening Post',
  'Yorksire Evening Post'  : 'Yorkshire Evening Post',
  'Yorkshire Evening post' : 'Yorkshire Evening Post',
  'Yorskhire Evening Post' : 'Yorkshire Evening Post',
  'Yorkshire Eveninig Post' : 'Yorkshire Evening Post',
  'yorkshire evening post' : 'Yorkshire Evening Post',
  'The yorkshire evening post' : 'Yorkshire Evening Post',
  'Yorkshire Post' : 'Yorkshire Post, The',
  'Yorkshire post' : 'Yorkshire Post, The',
  'The Yorkshire Post' : 'Yorkshire Post, The',
  'Yorkshire post culture' : 'Yorkshire Post, The',
  'Yorkshire  post' : 'Yorkshire Post, The',
  'Yorkshirepost' : 'Yorkshire Post, The',
  'Yorkshire post business' : 'Yorkshire Post, The',
  'Yorkshire Post - Business' : 'Yorkshire Post, The',
  'yorkshire post' : 'Yorkshire Post, The'
})
"""

combined_data.to_csv(OUTPUT_PATH,index=False)