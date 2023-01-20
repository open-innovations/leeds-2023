import os
import pandas as pd
from metrics.volunteers.process import summarise

from transform import SHIFT_DATA
from setup import VIEW_DIR


def prepare_shift_data():
    shifts = pd.read_csv(SHIFT_DATA, parse_dates=['date'])

    grouped = shifts.groupby('date')
    by_week = pd.DataFrame({
        'volunteers': grouped.attended.sum(),
        'hours': grouped.volunteer_hours.sum(),
    }).resample('W-FRI').sum().round().astype(int).reset_index()
    by_week.to_csv(os.path.join(VIEW_DIR, 'shifts_by_week.csv'), index=False)


if __name__ == "__main__":
    summarise()
    prepare_shift_data()
