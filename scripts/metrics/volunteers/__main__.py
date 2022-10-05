import os
import pandas as pd

from data import load_new_data, STATUS_APPLY, STATUS_OFFER, STATUS_CONFIRMED

print("Processing volunteers")


DATA_DIR = os.path.join('data', 'metrics', 'volunteers')
VIEW_DIR = os.path.join('docs', '_data', 'metrics', 'volunteers')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VIEW_DIR, exist_ok=True)

data = load_new_data()

data.ward_code.fillna('UNKNOWN', inplace=True)

data.to_csv(os.path.join(DATA_DIR, 'volunteers.csv'), index=False)

by_ward = data.groupby(['ward_code', 'status']).hash.count().unstack(level=1) \
  .fillna(0) \
  .astype(int)

by_ward.to_csv(os.path.join(VIEW_DIR, 'by_ward.csv'), na_rep=0)

# pd.DataFrame({
#     'total': by_ward.hash.count(),
#     STATUS_APPLY: data[data.status == STATUS_APPLY].groupby('ward_code').hash.count(),
#     STATUS_OFFER: data[data.status == STATUS_OFFER].groupby('ward_code').hash.count(),
#     STATUS_CONFIRMED: data[data.status == STATUS_CONFIRMED].groupby('ward_code').hash.count(),
# }).to_csv(os.path.join(VIEW_DIR, 'ward.csv'), na_rep=0)
