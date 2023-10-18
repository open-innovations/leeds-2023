import re
from lib.sources.airtable import query
from scripts.util.geography import fuzzy_match_leeds_wards


def fetch_data():
    BASE_ID = 'appHAh7IYG6p2w5Yo'
    TABLE_NAME = 'Schools'

    schools = query(BASE_ID, TABLE_NAME,
                    fields=[
                        'School Name',
                        'Postcode',
                        'Ward',
                    ])

    return schools.rename(columns=lambda x: re.sub(r'\W+', '_', x.lower()))


if __name__ == '__main__':
    data = fetch_data()
    data = fuzzy_match_leeds_wards(data)
    data.to_csv('data/reference/schools.csv', index=False)
