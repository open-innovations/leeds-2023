import pandas as pd
import os
import yaml

RAW_PATH = os.path.join('working','manual','hidden_stories','Hidden Stories Engagement Figures.xlsx')
LEEDS_WARDS_PATH = os.path.join('data','reference','leeds_wards.csv')
OUTPUT_DIR = os.path.join('docs','_data','metrics','hidden_stories')

data = pd.read_excel(RAW_PATH,nrows=10)

#Wards Count
leeds_wards = pd.read_csv(LEEDS_WARDS_PATH)
data['Ward'] = (data['Ward']
                .str.strip()
                .replace(['Chapeltown','Calverly and Farsley','Otley','Holbeck'],['Chapel Allerton','Calverley and Farsley','Otley and Yeadon','Beeston and Holbeck']))


ward_data = (pd.merge(data,leeds_wards,'left',left_on='Ward',right_on='WD21NM')
          .rename(columns={'WD21CD':'ward_code'})
          .groupby(by='ward_code'))

ward_file = os.path.join(OUTPUT_DIR,'wards.csv')
ward_data = pd.DataFrame({'count' : ward_data['WD21NM'].count(),
                          'audience_sum' : ward_data['Audience '].sum() ,
                          'participants_sum' : ward_data['Participants'].sum(),
                          'total_sum' : (ward_data['Audience '].sum() + ward_data['Participants'].sum())})
ward_data.to_csv(ward_file)

#Headline stats
stats = {'event_count' : int(data['Project '].count()), 
        'audience_sum' : int(data['Audience '].sum()), 
        'participants_sum' : int(data['Participants'].sum()),
        'audience_max' : int(data['Audience '].max()),
        'participants_max' : int(data['Participants'].max())}

with open(os.path.join(OUTPUT_DIR,'stats.yml'),'w') as f:
    yaml.safe_dump(stats,f)

print(stats)