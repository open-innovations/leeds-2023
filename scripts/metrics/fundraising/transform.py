import os
import pandas as pd

DATA_DIR = os.path.join('data', 'metrics', 'fundraising')
PIPELINE_FILE = os.path.join(DATA_DIR, 'pipeline.csv')
columns = {
    'id': 'id',
    'SectorTag': 'sector',
    'FundraisingStageTag': 'stage',
    'FundraisingBidStageSponsorTag': 'bid_stage_sponsor',
}


def load_extract():
    return pd.read_csv('working/fundraising/data_organisation_fundraising.csv',
                       usecols=columns.keys()).rename(columns=columns)


def transform(data):
    # Tidy up text
    data.sector = data.sector.str.title().fillna('Unknown')
    data.stage = data.stage.str.title().fillna('Unknown')
    data.bid_stage_sponsor = data.bid_stage_sponsor.fillna('Unknown')
    return data


def save_transformed(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    data[['id', 'sector', 'stage', 'bid_stage_sponsor']].to_csv(
        PIPELINE_FILE, index=False)


def load_transformed():
    return pd.read_csv(PIPELINE_FILE)


if __name__ == '__main__':
    data = load_extract()
    data = transform(data)
    save_transformed(data)
