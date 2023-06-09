import os

from lib.sources.ticket_tailor import get_orders

TICKET_RAW = os.path.join('working', 'metrics', 'ticketing')
os.makedirs(TICKET_RAW, exist_ok=True)

RAW_ORDER_FILE = os.path.join(TICKET_RAW, 'orders.csv')


if __name__ == '__main__':
    print('Getting orders')
    orders = get_orders()
    orders[
        [
            'object',
            'id',
            'postcode',
            'created_at',
            'event_id',
            'number_of_tickets',
            'referral_tag',
            'status',
            'status_message'
        ]
    ].to_csv(RAW_ORDER_FILE, index=False)
