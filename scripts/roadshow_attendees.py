from typeform import get_responses, get_field_from_item
from util import naive_postcode_formatter, write_csv
from util.date import round_to_nearest_hour
import pandas as pd


filename = './data/roadshow_attendees.csv'


def get_workshop_responses():
    form_id = 'vm2OxH3L'
    postcode_field_id = 'GHOzEy9LwD8o'
    workshop_data = get_responses(form_id, fields=postcode_field_id)

    def get_time_and_postcode(item):
        postcode = get_field_from_item(
            item, postcode_field_id)
        return {
            'datetime': item['submitted_at'],
            'postcode': naive_postcode_formatter(postcode)
        }

    data = [get_time_and_postcode(x) for x in workshop_data['items']]

    write_csv(data, filename,
              field_names=['datetime', 'postcode'])


def summarise():
    data = pd.read_csv(filename)
    data['datetime'] = data['datetime'].apply(round_to_nearest_hour)
    summary = data.groupby(by='datetime')['postcode'].apply(list)
    summary = summary.apply(lambda x: ';'.join([i for i in x if not pd.isnull(i)]))
    summary.to_csv('./data/roadshow_summary.csv')


if __name__ == '__main__':
    get_workshop_responses()
