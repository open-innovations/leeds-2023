import os
import pandas as pd
from typeform import get_field_from_item, get_responses
from util import naive_postcode_formatter


WORKING_DIR = os.path.join('working', 'roadshow')
CONTACT_CONSENT_RESPONSES = os.path.join(
    WORKING_DIR, 'contact_consent_responses.csv')

os.makedirs(WORKING_DIR, exist_ok=True)


def get_contact_consent_responses():
    form_id = 'vm2OxH3L'
    postcode_field_id = 'GHOzEy9LwD8o'
    roadshow_data = get_responses(form_id, fields=postcode_field_id)

    def get_time_and_postcode(item):
        postcode = get_field_from_item(
            item, postcode_field_id)
        return {
            'datetime': item['submitted_at'],
            'postcode': naive_postcode_formatter(postcode)
        }

    data = pd.DataFrame([get_time_and_postcode(x)
                        for x in roadshow_data['items']])
    data.to_csv(CONTACT_CONSENT_RESPONSES, index=False)


if __name__ == '__main__':
    get_contact_consent_responses()
