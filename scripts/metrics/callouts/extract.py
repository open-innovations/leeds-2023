import os
import pandas as pd
from util.firebase import pull_collection

STAGING_DIR = 'working/metrics/callouts/'

os.makedirs(STAGING_DIR, exist_ok=True)


def clean_callout(data):
    data = data.rename(columns={
      'dateSubmitted': 'date_submitted',
    })
    data.date_submitted = pd.DatetimeIndex(
        data.date_submitted).tz_localize(None).floor('D')
    return data


if __name__ == '__main__':
    
    data = pull_collection(
      collection_name=u'form-builder-submissions/dancersOfLeeds/responses',
      fields=[
        'dateSubmitted',
        'postcode',
      ])
    data = clean_callout(data)
    data.to_csv(STAGING_DIR + 'dancers_of_leeds.csv', index=False)
