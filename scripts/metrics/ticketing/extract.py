import os
import requests
from urllib.parse import urlparse
import pandas as pd

TICKET_RAW = os.path.join('working', 'metrics', 'ticketing')
os.makedirs(TICKET_RAW, exist_ok=True)

RAW_ORDER_FILE = os.path.join(TICKET_RAW, 'orders.csv')
RAW_EVENT_SERIES_FILE = os.path.join(TICKET_RAW, 'event_series.csv')
RAW_EVENT_OCCURRENCES_FILE = os.path.join(TICKET_RAW, 'event_occurrences.csv')


def replace_query(url, new_query):
    res = url.split('?')
    res[1] = new_query
    return '?'.join(res)


def ticket_tailor_api_call(url):
    data = []

    headers = {
        'Authorization': 'Basic {token}'.format(token=os.environ['TICKET_TAILOR_API_KEY']),
        'Accept': 'application/json',
    }

    while True:
        result = requests.request("GET", url, headers=headers).json()
        data = data + result['data']
        next_page = result['links']['next']
        if (next_page == None):
            break
        url = replace_query(url, urlparse(next_page).query)

    return pd.DataFrame(data)


def get_occurrences(series_ids):
    urls = ["https://api.tickettailor.com/v1/event_series/{id}/events?limit=100".format(
        id=id) for id in series_ids]
    return pd.concat([ticket_tailor_api_call(url) for url in urls])


if __name__ == '__main__':
    orders = ticket_tailor_api_call(
        "https://api.tickettailor.com/v1/orders?limit=100")

    orders['postcode'] = pd.json_normalize(orders.buyer_details)[
        'address.postal_code']
    orders['event_id'] = pd.json_normalize(orders.event_summary)['id']
    orders['number_of_tickets'] = orders.issued_tickets.apply(lambda x: len(x))
    orders.created_at = pd.to_datetime(orders.created_at, unit='s')

    orders[
        ['object', 'id', 'postcode', 'created_at', 'event_id', 'number_of_tickets',
            'referral_tag', 'status', 'status_message']
    ].to_csv(RAW_ORDER_FILE, index=False)

    events = ticket_tailor_api_call(
        "https://api.tickettailor.com/v1/event_series?limit=100?limit=100")

    events['postcode'] = pd.json_normalize(events.venue)['postal_code']

    events[
        ['object', 'id', 'name', 'online_event', 'private',
            'status', 'total_occurrences', 'postcode']
    ].to_csv(RAW_EVENT_SERIES_FILE, index=False)

    occurrences = get_occurrences(events.id.values)
    occurrences.start = pd.json_normalize(occurrences.start).iso
    occurrences.end = pd.json_normalize(occurrences.end).iso
    occurrences[
        ['object','id','event_series_id','tickets_available','total_issued_tickets','start','end','hidden','unavailable','unavailable_status'
]
    ].to_csv(RAW_EVENT_OCCURRENCES_FILE, index=False)
