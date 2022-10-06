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
