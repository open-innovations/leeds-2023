import json
import os

from dotenv import load_dotenv
from urllib.request import Request, urlopen

load_dotenv()

base_url = 'https://api.typeform.com'
headers = {
    'Authorization': 'Bearer {token}'.format(token=os.environ['TYPEFORM_PRIVATE_TOKEN'])
}


def get_responses(form_id, fields=''):
    url = '{base_url}/forms/{form_id}/responses?fields={fields}&page_size=1000'.format(
        base_url=base_url,
        form_id=form_id,
        fields=fields,
    )
    req = Request(url, headers=headers)
    with urlopen(req) as f:
        data = f.read().decode('utf-8')
    return json.loads(data)


def get_field_from_item(item, field_id):
    answers = item.get('answers', None)
    value = [x['text'] for x in answers if x['field']['id']
             == field_id].pop() if answers is not None else None
    return value
