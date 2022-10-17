import json
import requests
import pandas as pd
import sys

# 30 is max page size
TEMPLATE_URL_ORGANISATION_PAST = "https://www.eventbrite.co.uk/org/{}/showmore/?page_size=30&type=past&page={}"
TEMPLATE_URL_ORGANISATION_FUTURE = "https://www.eventbrite.co.uk/org/{}/showmore/?page_size=30&type=future&page={}"
URLS = [TEMPLATE_URL_ORGANISATION_PAST,TEMPLATE_URL_ORGANISATION_FUTURE]

def pull_events(org_id,attributes):
    events = []

    for url in URLS:
        page = 1
        has_next = True
        while has_next:
            result = requests.get(url.format(org_id,page)) 
            json_data = json.loads(result.text)
            events.extend(json_data["data"]["events"])
            has_next = json_data["data"]["has_next_page"]
            page += 1

    df = pd.json_normalize(events)
    df = df.filter(axis=1,items=attributes)
    return df

def main(org_id,attributes_path,out_path,sort=None):
    with open(attributes_path) as f:
        attributes = f.readline().split(",")

    events_df = pull_events(org_id,attributes)
    if sort is not None:
        events_df = events_df.sort_values(sort)

    events_df.to_csv(out_path,index=False)
    print(str(len(events_df)) + " events found.")

ORG_ID = 14487847966
ATTRIBUTES = ["id","slugified_name","venue.longitude","venue.latitude","start.utc","end.utc","online_event","description.text"]
ATTRIBUTES_PATH = "attrs.txt"
OUT_PATH = "test_filtered_test.csv"

if __name__ == "__main__":    
    org_id = sys.argv[1]
    attributes_path = sys.argv[2]
    out_path = sys.argv[3]
    sort = sys.argv[4]
    
    main(org_id,attributes_path,out_path,sort)


