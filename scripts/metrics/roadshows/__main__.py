from __future__ import print_function


import pandas as pd
from util.date import round_to_nearest_hour



def load_postcodes():
    return pd.read_csv(os.path.join('data', 'reference', 'postcodes.csv'))



def load_constituencies_2020():
    return pd.read_csv(os.path.join('data', 'reference', 'Westminster_Parliamentary_Constituencies_(December_2020)_UK_BFC.csv'))







def prepare_roadshow_data():
