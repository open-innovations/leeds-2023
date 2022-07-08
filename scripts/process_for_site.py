import pandas as pd


def process_workshop_attendees(freq='D'):
    data = pd.read_csv('data/roadshow_attendees_summary.csv',
                       parse_dates=['datetime'])
    # Summarises by required frequency and fills in gaps
    data = data.resample('W-Fri', on='datetime').sum().reset_index()
    print(data.datetime.name)
    data.rename(columns = {
      'datetime': 'week_ending'
    }, inplace=True)
    data['cumulative_attendees'] = data.attendees.cumsum()
    data.to_csv('docs/_data/roadshow_attendees_summary.csv',
                date_format="%Y-%m-%d", index=False)


def main():
    process_workshop_attendees('W-Mon')


if __name__ == '__main__':
    main()
