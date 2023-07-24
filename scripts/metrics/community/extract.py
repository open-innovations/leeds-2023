import os
import sys

TOP_DIR=os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../'))
if TOP_DIR not in sys.path: sys.path.append(TOP_DIR)

from lib.sources.airtable import query

DATA_DIR = os.path.join(TOP_DIR, 'working/metrics/community')

if __name__ == "__main__":
    # https://airtable.com/appHAh7IYG6p2w5Yo/shrId61ACMYGBg78W/tblQDTK5iBUkn3C0q
    data = query("appHAh7IYG6p2w5Yo", "tblQDTK5iBUkn3C0q", view="OI Community Engagement Evaluation Data")
    os.makedirs(DATA_DIR, exist_ok=True)
    data.to_csv(os.path.join(DATA_DIR, 'events.csv'), index=False)