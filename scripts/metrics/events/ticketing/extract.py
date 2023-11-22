import os
import sys

ROOT_DIR = os.path.abspath('../../../../')
lib_dir = os.path.join(ROOT_DIR, 'lib')
if lib_dir not in sys.path: sys.path.append(lib_dir)

from sources.ticket_tailor import get_orders
from pipes import process_orders


TICKET_RAW = os.path.join(ROOT_DIR, 'working', 'metrics', 'ticketing')
os.makedirs(TICKET_RAW, exist_ok=True)

RAW_ORDER_FILE = os.path.join(TICKET_RAW, 'orders.csv')


if __name__ == '__main__':
    print('Getting orders')
    orders = get_orders().pipe(process_orders)
    orders[
        [
            'object',
            'id',
            'postcode_from_question',
            'postcode_from_address',
            'created_at',
            'event_id',
            'event_name',
            'event_date',
            'event_time',
            'event_datetime',
            'number_of_tickets',
            'referral_tag',
            'status',
            'status_message'
        ]
    ].to_csv(RAW_ORDER_FILE, index=False)
