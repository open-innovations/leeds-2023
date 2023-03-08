import pandas as pd
from resolver import resolve_path

ATTENDEE_CSV = resolve_path('data/metrics/events/awakening/attendees.csv')

if __name__ == '__main__':
    data = pd.read_csv(ATTENDEE_CSV).rename(columns={
        'awakening_booked': 'booked',
        'awakening_attended': 'attended',
    })

    # Create summary
    data.set_index(['la_code', 'ward_code']).sum().to_json(
        resolve_path('docs/metrics/events/awakening/_data/attendees.json'))

    data.drop(
        columns=['la_code']
    ).groupby(['ward_code']).sum().to_csv(
        resolve_path(
            'docs/metrics/events/awakening/_data/attendees_by_ward.csv')
    )

    data.drop(
        columns=['ward_code']
    ).groupby(['la_code']).sum().to_csv(
        resolve_path(
            'docs/metrics/events/awakening/_data/attendees_by_la.csv')
    )
