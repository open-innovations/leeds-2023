import os
import pandas as pd

from metrics.fundraising.transform import load_transformed

SITE_DATA_PATH = os.path.join("docs", "_data", "metrics", "fundraising")


def summarise(data):
    os.makedirs(SITE_DATA_PATH, exist_ok=True)

    # Create summaries
    count_by_stage = pd.DataFrame({
        'stage': data.stage,
        'count': data.id,
    }).groupby(by=['stage']).count()
    count_by_stage.to_csv(os.path.join(SITE_DATA_PATH, 'count_by_stage.csv'))

    count_by_sector_and_stage = pd.DataFrame({
        'sector': data.sector,
        'stage': data.stage,
        'count': data.id,
    }).groupby(by=['sector', 'stage']).count()
    count_by_sector_and_stage.to_csv(os.path.join(
        SITE_DATA_PATH, 'count_by_sector_and_stage.csv'))


if __name__ == '__main__':
    data = load_transformed()
    summarise(data)
