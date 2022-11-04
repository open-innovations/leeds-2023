import pandas as pd


def process():
    data = pd.read_excel('working/LEEDS 2023 Fundraising Progress.xlsx',
      sheet_name='Progress', skiprows=3,
      usecols=[
        'Organisation/Individual', 'Project',
        'Funding type', 'Restricted/ Unrestricted',
        'Application status',
        'Amount '
      ])
    data = data[data['Amount '].notna()]
    data['Application status'] = data['Application status'].fillna('UNKNOWN').str.upper().str.strip()
    data['Organisation/Individual'] = data['Organisation/Individual'].str.strip()
    data = data[~data['Application status'].str.match(r'^TOTAL')]

    by_stage = pd.DataFrame({
      'amount': data.groupby('Application status')['Amount '].sum()
    })
    by_stage.index.name='status'
    by_stage.to_csv('data/metrics/fundraising/amount_by_stage.csv')
