from pathlib import Path
import lib.sources.airtable as airtable

WORKING_DIR = Path(__file__).parent.joinpath('../../../working/metrics/partnerships').resolve()

def extract(output_dir: str | Path):
    if type(output_dir == 'str'):
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = airtable.query(
      base_id='appErAjqETTDMm2xU',
      table_name='tblFx3Uch6PBF94uq'
    )
    
    data.rename(
        columns = lambda c: c.strip()
    ).to_csv(
        output_dir.joinpath('all.csv'),
        index=False
    )
  

if __name__ == "__main__":
    extract(WORKING_DIR)
    

#     data = airtable.events(
#         fields=[
#             'Event Unique Identifier',
#             'AirTable ID',
#             'Event name',
#             'Project name',
#             'Project type',
#             'Event type',
#             'Season',
#             'Start date',
#             'End date',
#             'Postcode (from Venue)',
#             'Ward (from Venue)',
#             'ACTUAL Audience size / number of participants - IN PERSON',
#             'ACTUAL Audience size / number of participants - ONLINE',
#             'Number of booked participants',
#             'Ticket Tailor ID',
#         ])

#     data.to_csv(os.path.join(WORKING_DIR, 'all.csv'), index=False)
