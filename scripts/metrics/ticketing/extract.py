import os
import requests
from urllib.parse import urlparse
import pandas as pd

TICKET_RAW = os.path.join('working', 'metrics', 'ticketing')
os.makedirs(TICKET_RAW, exist_ok=True)

RAW_EVENT_FILE = os.path.join(TICKET_RAW, 'event_series.csv')
RAW_ORDER_FILE = os.path.join(TICKET_RAW, 'orders.csv')


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


if __name__ == '__main__':
    orders = ticket_tailor_api_call(
        "https://api.tickettailor.com/v1/orders?limit=100")
    orders[
        ['object', 'id', 'buyer_details', 'created_at', 'event_summary', 'issued_tickets',
            'line_items', 'referral_tag', 'status', 'status_message', 'txn_id']
    ].to_csv(RAW_ORDER_FILE, index=False)

    events = ticket_tailor_api_call(
        "https://api.tickettailor.com/v1/event_series?limit=100?limit=100")
    events[
        ['object', 'id', 'created_at', 'name', 'online_event', 'private',
            'status', 'timezone', 'total_occurrences', 'venue']
    ].to_csv(RAW_EVENT_FILE, index=False)
