import os
import re
import pandas as pd

EVENT_MASTER = os.path.join("working", "manual", "activity", "Leeds 2023 activity logging MASTER.xlsx")
DATA_DIR = os.path.join("data", "metrics", "activity")
EVENT_EXTRACT = os.path.join(DATA_DIR, "activity_log_extract.csv")

column_map = {
  'Event ID': 'event_id',
  'Activity name': 'activity_name',
  'Is this activity part of a Signature project or a series of different activities under the same banner?': 'is_series',
  'If Yes, what is the name of the Signature project or series of different activities under the same banner?': 'series_name',
  'Is this activity a one off, or is it repeated (e.g. multiple performances of same work)?': 'repeated',
  'If it is repeated, how many times?': 'repeats',
  'What is the activity category?': 'category',
  'What is the activity artform or type of culture?': 'artform',
  'What was the activity date or first date? (DD/MM/YYYY)': 'start_date',
  'What was the activity end date IF APPLICABLE? (DD/MM/YYYY)': 'end_date',
  'What was the venue or location of the activity?': 'venue',
  'Postcode for venue / location': 'postcode',
  'Audience size / number of participants - IN-PERSON': 'audience_in_person',
  'Audience size / number of participants - ONLINE': 'audience_online',
  'Participation type': 'participation_type',
}

def load_activity_log():
    data = pd.read_excel(EVENT_MASTER, sheet_name="Activity log", skiprows=4)
    data.drop(columns=[v for v in data.columns.values if re.search(r'^Unnamed', v)], inplace=True)
    data = data[~data['Activity name'].isna()]
    return data


def reformat_data(data):
    data = data[column_map.keys()].rename(columns=column_map)
    return data


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    activity = load_activity_log()

    activity = reformat_data(activity)

    activity.to_csv(EVENT_EXTRACT, index=False)