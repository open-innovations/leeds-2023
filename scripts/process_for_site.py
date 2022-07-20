import pandas as pd
import shutil
import metrics.media_coverage


def process_workshop_attendees(freq='D'):
    data = pd.read_csv('data/roadshow_attendees_summary.csv',
                       parse_dates=['datetime'])
    # Summarises by required frequency and fills in gaps
    data = data.resample('W-Fri', on='datetime').sum().reset_index()

    data.rename(columns={
        'datetime': 'week_ending'
    }, inplace=True)

    data = pd.concat([
        data,
        pd.DataFrame.from_records([{
            'week_ending': data.week_ending.min() - pd.Timedelta(weeks=1),
            'attendees': 0
        }])
    ]).sort_values('week_ending')

    data['cumulative_attendees'] = data.attendees.cumsum()

    data.to_csv('docs/_data/metrics/roadshow_attendees/summary.csv',
                date_format="%Y-%m-%d", index=False)

    shutil.copy('data/roadshow_attendees_count_by_ward.csv', 'docs/_data/metrics/roadshow_attendees/by_ward.csv')


def main():
    process_workshop_attendees('W-Mon')
    metrics.media_coverage.summarise()

if __name__ == '__main__':
    main()
