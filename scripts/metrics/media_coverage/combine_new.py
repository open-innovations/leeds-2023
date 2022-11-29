import pandas as pd
import os

MASTER_FILE_PATH = os.path.join('data','metrics','media_coverage','combined.csv')
NEW_FILE_PATH = os.path.join('working','manual','media','Leeds 2023 weekly media coverage.csv')


master = pd.read_csv(MASTER_FILE_PATH,parse_dates=['News Date'])
new = pd.read_csv(NEW_FILE_PATH,parse_dates=['News Date'],dayfirst=True)

#contact name, outlet type, custom tags, news text =  missing from new
# new colum: News Attachment Name

combined = pd.concat([master,new]).drop(columns=['News Attachment Name']).sort_values(by=['News Date','News Headline','Medium'])
combined['Audience Reach'] = combined['Audience Reach'].astype('Int64')
combined['UV*'] = combined['UV*'].astype('Int64')
combined.to_csv(MASTER_FILE_PATH,index=False)