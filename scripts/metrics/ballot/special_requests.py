import os
import logging

import pandas as pd
from metrics.ballot.firebase import get_db

TEMP_DIR = 'working/metrics/ballot'
def fiona_2022_10_18():
    db = get_db()
    ballot_ref = db.collection(u'ballot-entries')

    logging.info("Querying ballot database")
    docs = ballot_ref.select([
        'dateSubmitted',
        'source',
    ]).stream()

    # Create a dataframe
    data = pd.DataFrame([doc.to_dict() for doc in docs])
    logging.info("Got %d entries", data.shape[0])

    # Convert and round the date
    data.dateSubmitted = pd.DatetimeIndex(
        data.dateSubmitted).tz_localize(None).floor('D')

    # data.groupby(['source', 'dateSubmitted'])
    # data = data.resample('D', on='dateSubmitted').source.count()
    data = pd.DataFrame({
      'count': data.groupby(['dateSubmitted', 'source']).source.count()
    })

    os.makedirs(TEMP_DIR, exist_ok=True)
    data.to_csv(os.path.join(TEMP_DIR, 'source.csv'))

fiona_2022_10_18()