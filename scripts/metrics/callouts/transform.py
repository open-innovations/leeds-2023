import os
import pandas as pd
from extract import STAGING_DIR
import util.geography as geo

DATA_DIR='data/metrics/callouts/'
os.makedirs(DATA_DIR, exist_ok=True)


if __name__ == '__main__':
    data_dol = pd.read_csv(STAGING_DIR + 'dancers_of_leeds.csv')
    data_dol = geo.match_ward(data_dol)
    data_dol = data_dol.drop(columns=['postcode'])
    data_dol.to_csv(DATA_DIR + 'dancers_of_leeds.csv', index=False)
