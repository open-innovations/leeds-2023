import os
from functools import reduce

import pandas as pd
from util.firebase import pull_collection
from util.logger import logging

logger = logging.getLogger(__name__)

STAGING_DIR = 'working/metrics/community-grants/'

os.makedirs(STAGING_DIR, exist_ok=True)


def clean_callout(data):
    data = data.rename(columns={
        'dateSubmitted': 'date_submitted',
        'schoolPostcode': 'postcode',
        'grantApplicantWard': 'ward',
        'grantApplicantInfo': 'type',
    })
    
    # Remove test data
    # TODO actually get there removed at source
    pre_count = len(data.index)
    data = data[
        data.postcode != 'test'
    ]
    diff = pre_count - len(data.index)
    if diff > 0:
        logger.warning('Removing %d test entries', diff)

    data.date_submitted = pd.DatetimeIndex(
        data.date_submitted).tz_localize(None).floor('D')
    
    return data


def camel_to_snake_case(str):
    return reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, str).lower()


if __name__ == '__main__':
    forms = [
        u'myLeedsGrantApp',
        u'myLeedsGrantAppAudiovisual',
        u'myLeedsSchoolsGrantsApplication'
    ]

    for form in forms:
        logger.info('Processing %s', form)
        collection_name = u'form-builder-submissions/{}/responses'.format(
            form)
        key = camel_to_snake_case(form)
        data = pull_collection(
            collection_name=collection_name,
            fields=[
                'id',
                'dateSubmitted',
                'postcode',
                'schoolPostcode',
                'grantApplicantWard',
                'grantApplicantInfo',  
            ])
        data = clean_callout(data)
        data.to_csv(os.path.join(
            STAGING_DIR, key + '.csv'), index=False)
