import logging
from datetime import datetime

import pandas as pd

STATUS_PRE_APPLY = 'created'
STATUS_APPLY = 'applied'
STATUS_OFFER = 'offered'
STATUS_CONFIRMED = 'confirmed'
STATUS_DROP = 'rejected'


def map_checkpoints_to_states(series):
    return series.replace({
        '1 Default': STATUS_PRE_APPLY,
        '2 Application Completed (HOLDING)': STATUS_APPLY,
        '2b Partner Profile Completed (HOLDING)': STATUS_APPLY,
        '2c Student Profile Completed (HOLDING)': STATUS_APPLY,
        '2d Neighbourhood Host Profile Complete (HOLDING)': STATUS_APPLY,
        '2e Team Leader Profile Completed (HOLDING)': STATUS_APPLY,
        '3 Invite to Meeting Session': STATUS_APPLY,
        '3b NO Invite to Meeting Session': STATUS_DROP,
        '3c NO Attendance at Meeting Session': STATUS_DROP,
        '4 Attended Meeting Session (HOLDING)': STATUS_APPLY,
        '5 Invite to Induction': STATUS_OFFER,
        '5b NO Invite to Induction': STATUS_DROP,
        '5c NO Attendance at Induction': STATUS_DROP,
        '6 Confirmed Volunteer': STATUS_CONFIRMED,
    })


def add_states(data):
    # Append columns to hold states
    states = pd.DataFrame(columns=[
        STATUS_PRE_APPLY,
        STATUS_APPLY,
        STATUS_OFFER,
        STATUS_CONFIRMED,
        STATUS_DROP,
    ], dtype='datetime64[ns]')
    return pd.concat([data, states])


def update_states(data):
    logging.info('Processing %d entries', len(data))
    data = set_created_date(data)
    data = set_applied_date(data)
    # data = override_state_date(data, STATUS_APPLY)
    data = set_offer_date(data)
    data = set_confirmed_date(data)
    data = set_dropped_date(data)

    data.drop(columns=['sign_up_date', 'modified'], inplace=True)
    return data


def set_created_date(data):
    # Set created date to sign up date
    data.loc[
        data[STATUS_PRE_APPLY].isnull(),
        STATUS_PRE_APPLY
    ] = data.sign_up_date.dt.floor('D')

    return data


def override_state_date(data, state=STATUS_APPLY, modified='modified'):
    '''Set applied date to modified date if status date is null'''
    # NB initial load assumed that the modified date is the time of the status change - as at 5th October
    data.loc[
        (data[state].isnull()) &
        (data.status.isin([state])), state] = data[modified].dt.floor('D')
    return data


def set_status_to_now(data, status, future_states):
    data.loc[
        (data[status].isnull()) & (data.status.isin(future_states)),
        status
    ] = pd.Timestamp.now().floor('D')
    return data


def set_applied_date(data):
    return set_status_to_now(data, STATUS_APPLY, [STATUS_APPLY, STATUS_OFFER, STATUS_CONFIRMED, STATUS_DROP])


def set_offer_date(data):
    return set_status_to_now(data, STATUS_OFFER, [STATUS_OFFER, STATUS_CONFIRMED])


def set_confirmed_date(data):
    return set_status_to_now(data, STATUS_CONFIRMED, [STATUS_CONFIRMED])


def set_dropped_date(data):
    return set_status_to_now(data, STATUS_DROP, [STATUS_DROP])
