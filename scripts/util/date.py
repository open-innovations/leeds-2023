from datetime import datetime, timedelta
from dateutil.parser import isoparse


def round_to_nearest_hour(dt):
    if type(dt) is not datetime:
        dt = isoparse(dt)
    dt = dt.replace(minute=0, second=0, microsecond=0) + \
        timedelta(hours=dt.minute//30)
    return dt
