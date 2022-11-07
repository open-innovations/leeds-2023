import pandas as pd


def process():
    data = pd.read_excel('working/LEEDS 2023 Fundraising Progress.xlsx',
      sheet_name='Progress', skiprows=3,
      usecols=[
        'Date Applied',
        'Organisation/Individual', 'Project',
        'Funding type', 'Restricted/ Unrestricted',
        'Application status',
        'Amount '
      ])
    data = data.rename(columns={'Date Applied' : 'type', 'Application status' : 'status' })
    data['type'] = data['type'].replace('Oct 2021','TRUSTS AND FOUNDATIONS').fillna(method='ffill')
    data = data[data['Amount '].notna()]
    data['status'] = data['status'].fillna(method='backfill').str.upper().str.strip()
    data.loc[(data['Organisation/Individual'].notna()),'status'] = data.loc[(data['Organisation/Individual'].notna()),'status'].str.replace('TOTAL ','')
    data['Organisation/Individual'] = data['Organisation/Individual'].str.strip()
    data = data[~data['status'].str.match(r'^TOTAL')]
   
    by_stage = pd.DataFrame({
      'amount': data.groupby('status')['Amount '].sum()
    })
    by_stage.to_csv('data/metrics/fundraising/amount_by_stage.csv')


    by_stage_and_type = pd.DataFrame({
      'amount': data.groupby(['type','status'])['Amount '].sum()
    })
    print(by_stage_and_type)
    by_stage_and_type.to_csv('data/metrics/fundraising/amount_by_stage_and_type.csv')
