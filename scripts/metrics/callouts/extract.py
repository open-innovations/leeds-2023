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
    callouts = [
      {
        'key': 'dancers_of_leeds',
        'collection': u'form-builder-submissions/dancersOfLeeds/responses',
      },
      {
        'key': 'leeds_on_wheels',
        'collection': u'form-builder-submissions/leedsOnWheels/responses',
      }
    ]

    for callout in callouts:
        data = pull_collection(
          collection_name=callout['collection'],
          fields=[
            'dateSubmitted',
            'postcode',
          ])
        data=clean_callout(data)
        data.to_csv(os.path.join(
            STAGING_DIR, callout['key'] + '.csv'), index = False)
