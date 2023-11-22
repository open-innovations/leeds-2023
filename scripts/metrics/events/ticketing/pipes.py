import pandas as pd


def process_orders(data):
    data['postcode_from_question'] = pd.json_normalize(data.buyer_details).custom_questions.map(
        lambda q: next((x['answer'] for x in q if x['question'] == 'Postcode'), None))
    data['postcode_from_address'] = pd.json_normalize(
        data.buyer_details)['address.postal_code']
    data['event_id'] = pd.json_normalize(data.event_summary)['id']
    data['event_name'] = pd.json_normalize(data.event_summary)['name']
    data['event_date'] = pd.json_normalize(data.event_summary)['start_date.date']
    data['event_time'] = pd.json_normalize(data.event_summary)['start_date.time']
    data['event_datetime'] = pd.json_normalize(data.event_summary)['start_date.iso']
    data['number_of_tickets'] = data.issued_tickets.apply(lambda x: len(x))
    data.created_at = pd.to_datetime(data.created_at, unit='s')
    return data
