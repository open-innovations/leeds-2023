import os
import lib.sources.airtable as airtable

WORKING_DIR = os.path.join('working', 'metrics', 'events')
os.makedirs(WORKING_DIR, exist_ok=True)

if __name__ == "__main__":
    data = airtable.events(
        fields=[
            'Event Unique Identifier',
            'AirTable ID',
            'Event name',
            'Project name',
            'Project type',
            'Event type',
            'Season',
            'Start date',
            'End date',
            'Postcode (from Venue)',
            'Ward (from Venue)',
            'ACTUAL Audience size / number of participants - IN PERSON',
            'ACTUAL Audience size / number of participants - ONLINE',
            'Number of booked participants',
        ])

    data.to_csv(os.path.join(WORKING_DIR, 'all.csv'), index=False)
