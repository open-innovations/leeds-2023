import os
import pandas as pd

TICKET_FILE = os.path.abspath(os.path.join(os.path.dirname(
    __file__), '../../../../data/metrics/events/tickets/orders.csv'))
orders = pd.read_csv(TICKET_FILE, index_col='event_id',
                     parse_dates=['created_at', 'event_date'])


def get_tickets_for_project(project):
    if type(project) == str:
        return orders.loc[orders.project_name == project, :]
    return orders.loc[orders.project_name.isin(project), :]


def filter_public_events(data):
    return data.loc[data.public_event == True, :]


def get_tickets_for_event(data: pd.DataFrame) -> pd.DataFrame:
    '''Extracts a table of ticket purchases linked cross-referened by airtable ID'''
    return (
        data
        .reset_index()
        .set_index('airtable_id')
        .ticket_tailor_id
        .str.replace(r'[\,\s]+', ' ', regex=True)
        .str.split()
        .explode()
        .to_frame()
        .reset_index()
        .set_index('ticket_tailor_id')
        .join(orders, how='inner')
        .reset_index()
    )


def _summarise_by(data: pd.DataFrame, column: str) -> pd.DataFrame:
    '''Summarise ticketing data by a defined column'''
    return pd.DataFrame({
        'orders': data.groupby(column).number_of_tickets.count(),
        'tickets': data.groupby(column).number_of_tickets.sum()
    })


def summarise_by_ward(data: pd.DataFrame) -> pd.DataFrame:
    '''Summarise ticketing data by ward code'''
    return data.pipe(_summarise_by, 'ward_code')


def summarise_by_date(data):
    '''Summarise ticketing data by date'''
    return data.rename(columns={
        'created_at': 'date'
    }).pipe(
        _summarise_by, 'date'
    ).resample('D').sum()
