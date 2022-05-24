import csv
import re

def write_csv(data, filename, field_names=None):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)


def naive_postcode_formatter(postcode):
    if postcode is not None:
        postcode = re.sub(
            r'^([A-Z]+)(\d+)\s*(\d)([A-Z]{2})', r'\1\2 \3\4', postcode.upper())
        return postcode