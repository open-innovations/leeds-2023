import logging
import os

from metrics.volunteers.data import load_new_data, load_raw_data, save_raw_data
from metrics.volunteers.metadata import MetadataReader
from metrics.volunteers.setup import DATA_DIR, META_DIR
from metrics.volunteers.states import update_states


def update():
    logging.info('Loading data')
    data = load_raw_data()
    new_data = load_new_data()

    logging.info('Combining data')
    # Capture some stats
    old_rowcount = data.shape[0]
    new_rowcount = new_data.shape[0]

    # Copy the status, ward code and la code to new columns
    new_data['new_status'] = new_data.status
    new_data['new_ward_code'] = new_data.ward_code
    new_data['new_local_authority_code'] = new_data.local_authority_code

    # Merge the datasets! data wins!
    data = data.combine_first(new_data)

    # Count how many rows have changed (i.e. were in the old dataset and have new status)
    changed_rowcount = data[data.status != data.new_status].shape[0]

    # Check if the record is still current
    data['current'] = data.index.isin(new_data.index)

    # Overwrite the status column
    data.status = data.new_status
    data.ward_code = data.new_ward_code.fillna('UNKNOWN')
    data.local_authority_code = data.new_local_authority_code.fillna('UNKNOWN')

    # Remove the new_* columns
    data.drop(columns=['new_status', 'new_ward_code',
              'new_local_authority_code'], inplace=True)

    logging.info('Adding {new} and updating status for {changes} volunteers'.format(
        new=new_rowcount - old_rowcount,
        changes=changed_rowcount
    ))

    logging.info('Updating dates for the states')
    data = update_states(data)

    save_raw_data(data)


if __name__ == "__main__":
    update()
    volunteer_metadata = MetadataReader(
        os.path.join(DATA_DIR, 'volunteers.csv'),
        base=DATA_DIR,
        dimensions=[],
        facts=['hash', 'created', 'applied', 'applied',
               'offered', 'confirmed', 'rejected']
    ).save_metadata(META_DIR)
