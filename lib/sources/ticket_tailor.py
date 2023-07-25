import os
from urllib.parse import urlparse

import pandas as pd
import requests
from ratelimit import limits, sleep_and_retry

API_KEY = os.environ['TICKET_TAILOR_API_KEY']


def replace_query(url, new_query):
    res = url.split('?')
    res[1] = new_query
    return '?'.join(res)


@sleep_and_retry
@limits(calls=20, period=36)
def limited_call(*args, **kwargs):
    response = requests.request(*args, **kwargs)
    return response


def call_api(url):
    data = []

    headers = {
        'Authorization': 'Basic {token}'.format(token=API_KEY),
        'Accept': 'application/json',
    }

    while True:
        result = limited_call("GET", url, headers=headers).json()
        try:
            data = data + result['data']
            next_page = result['links']['next']
            if (next_page == None):
                break
            url = replace_query(url, urlparse(next_page).query)
        except:
            print(result)

    return pd.DataFrame(data)


def get_orders():
    orders = call_api("https://api.tickettailor.com/v1/orders?limit=100")
    return orders


def get_events():
    events = call_api("https://api.tickettailor.com/v1/event_series?limit=100")

    events['postcode'] = pd.json_normalize(events.venue)['postal_code']
    return events


def get_occurrences(series_ids):
    urls = [
        "https://api.tickettailor.com/v1/event_series/{id}/events?limit=100".format(
            id=id)
        for id
        in series_ids
    ]

    occurrences = pd.concat([call_api(url) for url in urls])
    occurrences.start = pd.json_normalize(occurrences.start).iso
    occurrences.end = pd.json_normalize(occurrences.end).iso

    return occurrences
