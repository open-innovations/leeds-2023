import pandas as pd
import os
import glob

WORKING_DIR = os.path.join('working','manual','media')
OUTPUT_FILE_PATH = os.path.join('data','metrics','media_coverage','combined_cision.csv')


files = glob.glob(os.path.join(WORKING_DIR, '*.csv'))

dfs = [pd.read_csv(file,parse_dates=['News Date'],dayfirst=True) for file in files]

columns_order = ['News Date','News Headline','Outlet Name','Audience Reach','UV*','Tone','Medium','Outlet Type','Custom Tags','News Company Mentions']
combined_data = (pd.concat(dfs)
                    .drop(columns=['News Text','Contact Name','News Attachment Name'])
                    .sort_values(by=['News Date','News Headline','Medium'])
                    .reindex(columns=columns_order))

combined_data['UV*'] = combined_data['UV*'].astype('Int64')
combined_data.columns = combined_data.columns.str.replace(' ','_').str.replace('*','',regex=False).str.lower()


combined_data.to_csv(OUTPUT_FILE_PATH,index=False)