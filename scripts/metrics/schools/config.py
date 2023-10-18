import os
import ast


WORKING_DIR = os.path.join('working', 'metrics', 'airtable')
DATA_DIR = os.path.join("data", "metrics", "schools")

os.makedirs(WORKING_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

RAW_SCHOOLS_DATA = os.path.join(WORKING_DIR, 'schools_events.csv')
SCHOOLS_DATA = os.path.join(DATA_DIR, 'schools_events.csv')


def literal_converter(series):
    def convert(value):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value
    return series.apply(convert)
