import os
from urllib.parse import urlparse

import pandas as pd
import requests

API_KEY = os.environ['TICKET_TAILOR_API_KEY']


def replace_query(url, new_query):
    res = url.split('?')
    res[1] = new_query
    return '?'.join(res)


def call_api(url):
    data = []

    headers = {
        'Authorization': 'Basic {token}'.format(token=API_KEY),
        'Accept': 'application/json',
    }

    while True:
        result = requests.request("GET", url, headers=headers).json()
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
    orders['postcode'] = pd.json_normalize(orders.buyer_details)[
        'address.postal_code']
    orders['event_id'] = pd.json_normalize(orders.event_summary)['id']
    orders['number_of_tickets'] = orders.issued_tickets.apply(lambda x: len(x))
    orders.created_at = pd.to_datetime(orders.created_at, unit='s')
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
