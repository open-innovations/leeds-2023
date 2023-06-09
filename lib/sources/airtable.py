import os
import pandas as pd
from pyairtable import Table

API_KEY = os.environ['AIRTABLE_API_KEY']
BASE_ID = 'appHAh7IYG6p2w5Yo'
EVENTS_TABLE = 'EVENTS'

events_table = Table(API_KEY, BASE_ID, EVENTS_TABLE)

def events(**kwargs):
    data = events_table.all(**kwargs)
    return pd.json_normalize([x['fields'] for x in data])
