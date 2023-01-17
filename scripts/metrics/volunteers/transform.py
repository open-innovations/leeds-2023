import os
import pandas as pd
from metrics.volunteers.process import update
from metrics.volunteers.setup import DATA_DIR

SHIFT_HOURS_RAW = os.path.join(
    'working', 'manual', 'volunteers', 'volunteering-hours.csv')
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
    data['volunteer_hours'] = (data.demand_hours / data.demand * data.attended).round(3)

    data = data[[
      'date',
      'shift_id',
      'postcode',
      'volunteer_hours',
      'attended',
      'demand',
      'event_id',
      'event_name',
    ]].sort_values(['date'])

    data.to_csv(SHIFT_DATA)


if __name__ == "__main__":
    update()
    transform_shift_hours()
