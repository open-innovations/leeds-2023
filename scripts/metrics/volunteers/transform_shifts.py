import os
import pandas as pd
from metrics.volunteers.setup import WORKING_DIR, DATA_DIR

SHIFT_HOURS_RAW = os.path.join(
    WORKING_DIR, 'volunteering-hours.csv')
SHIFT_DATA = os.path.join(
    DATA_DIR, 'shifts.csv'
)


def transform_shift_hours():
    shift_column_renamer = {
        'Event - ID': 'event_id',
        'Event - Name': 'event_name',
        'Event - Type': 'event_type',
        'Event Shift - ID': 'shift_id',
        'Event Shift - Postal Code': 'postcode',
        'Event Shift - Date/Time From': 'shift_start',
        'Event Shift - Date/Time To': 'shift_end',
        'Event Shift - Demand': 'demand',
        'Event Shift - Hours': 'demand_hours',
        'Event Shift - Attended': 'attended',
    }
    data = pd.read_csv(SHIFT_HOURS_RAW, parse_dates=[
        'Event Shift - Date/Time From',
        'Event Shift - Date/Time To',
    ]).rename(columns=shift_column_renamer)
    data = data[data.attended > 0]

    data['date'] = data.shift_start.dt.floor(freq='D')
    data['volunteer_hours'] = (
        data.demand_hours / data.demand * data.attended).round(3)

    data = data[[
        'date',
        'shift_id',
        'postcode',
        'volunteer_hours',
        'attended',
        'demand',
        'event_id',
        'event_name',
        'event_type',
    ]].sort_values(['date', 'shift_id'])

    data.event_type = data.event_type.map({
        "LEEDS 2023 Events": "LEEDS 2023 Events",
        "Partner Events": "Partner Events"
    })

    data.to_csv(SHIFT_DATA, index=False)


if __name__ == "__main__":
    transform_shift_hours()
