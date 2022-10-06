import logging
import pandas as pd
from metrics.volunteers.states import STATUS_PRE_APPLY, STATUS_APPLY, STATUS_OFFER, STATUS_CONFIRMED, STATUS_DROP


def summarise_by_ward(data, file_path):
    logging.info('Summarising by ward')
    by_ward = data.groupby(['ward_code'])
    by_ward = pd.DataFrame({
        STATUS_PRE_APPLY: by_ward[STATUS_PRE_APPLY].count(),
        STATUS_APPLY: by_ward[STATUS_APPLY].count(),
        STATUS_OFFER: by_ward[STATUS_OFFER].count(),
        STATUS_CONFIRMED: by_ward[STATUS_CONFIRMED].count(),
        STATUS_DROP: by_ward[STATUS_DROP].count(),
    }).fillna(0).astype(int)
    logging.info('Writing `%s`', file_path)
    by_ward.to_csv(file_path, na_rep=0)


def summarise_by_week(data, file_path):
    logging.info('Summarising by week')
    data = data.reset_index()
    by_date = pd.DataFrame({
        STATUS_PRE_APPLY: data.groupby(STATUS_PRE_APPLY).hash.count(),
        STATUS_APPLY: data.groupby(STATUS_APPLY).hash.count(),
        STATUS_OFFER: data.groupby(STATUS_OFFER).hash.count(),
        STATUS_CONFIRMED: data.groupby(STATUS_CONFIRMED).hash.count(),
        STATUS_DROP: data.groupby(STATUS_DROP).hash.count(),
    })
    by_date.index = by_date.index.astype('datetime64[ns]')
    by_date.index.names = ['week_ending']
    by_date = by_date.resample('W-Fri').sum().fillna(0).astype(int)
    logging.info('Writing `%s`', file_path)
    by_date.cumsum().to_csv(file_path, na_rep=0)
