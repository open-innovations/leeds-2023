import os
from pyairtable import Table
import pyairtable.formulas as f
import pandas as pd


def fetch_data(base_id, table_name, view_name=None, fields=None):
    API_KEY = os.environ['AIRTABLE_API_KEY']

    table = Table(API_KEY, base_id, table_name)

    data = table.all(
        view=view_name,
        fields=fields)
    return pd.json_normalize([x['fields'] for x in data])
