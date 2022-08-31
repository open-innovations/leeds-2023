import os
import pandas as pd
import shutil

columns = [
    "id",
    "SectorTag",
    "FundraisingStageTag",
    "FundraisingBidStageSponsorTag",
]

data_dir = os.path.join('data', 'metrics', 'fundraising')
SITE_DATA_PATH = os.path.join("docs", "_data", "metrics", "fundraising")


def process(source_path):
    data = pd.read_csv(source_path, usecols=columns)

    # Tidy up text
    data.SectorTag = data.SectorTag.str.title()
    data.FundraisingStageTag = data.FundraisingStageTag.str.title()

    # Create summaries
    count_by_stage = pd.DataFrame({
        'stage': data.FundraisingStageTag,
        'count': data.id,
    }).groupby(by=['stage']).count()
    count_by_sector_and_stage = pd.DataFrame({
        'sector': data.SectorTag,
        'stage': data.FundraisingStageTag,
        'count': data.id,
    }).groupby(by=['sector', 'stage']).count()

    working_dir = os.getcwd()

    os.makedirs(data_dir, exist_ok=True)
    os.chdir(data_dir)
    count_by_stage.to_csv('count_by_stage.csv')
    count_by_sector_and_stage.to_csv('count_by_sector_and_stage.csv')

    os.chdir(working_dir)


def copy_to_site():
    shutil.copytree(data_dir, SITE_DATA_PATH, dirs_exist_ok=True)
