import os
import pandas as pd
from util.geography import match_ward, match_la

RAW_DATA = 'working/manual/events/Awakening/THE AWAKENING BOOKER DATA ANON.xlsx'
OUT_DIR = 'data/metrics/events/awakening/'
os.makedirs(OUT_DIR, exist_ok=True)
DATA_FILE = os.path.join(OUT_DIR, 'attendees.csv')

if __name__ == '__main__':
    data = pd.read_excel(RAW_DATA, sheet_name='FINAL DATA (Customers)', usecols=[0,1,2])
    data.rename(columns=str.lower, inplace=True)
    data = match_ward(data)
    data = match_la(data)
    data[[
        'la_code', 'ward_code', 'awakening_booked', 'awakening_attended'
    ]].sort_values(['la_code', 'ward_code']).to_csv(DATA_FILE, index=False)