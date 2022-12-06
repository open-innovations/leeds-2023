import os
from functools import reduce

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


def camel_to_snake_case(str):
    return reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, str).lower()


if __name__ == '__main__':
    callouts = [
        u'dancersOfLeeds',
        u'leedsOnWheels',
        u'authorsAbroad',
        u'awakeningHospitality',
        u'becomeAWowser',
        u'earlyCareerMusicPromoters',
        u'leedsYoungFilm',
        u'offTheCurriculum',
    ]

    for callout in callouts:
        collection_name = u'form-builder-submissions/{}/responses'.format(
            callout)
        key = camel_to_snake_case(callout)
        data = pull_collection(
            collection_name=collection_name,
            fields=[
                'dateSubmitted',
                'postcode',
            ])
        data = clean_callout(data)
        data.to_csv(os.path.join(
            STAGING_DIR, key + '.csv'), index=False)
