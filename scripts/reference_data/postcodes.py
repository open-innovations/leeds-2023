import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)

CENTROIDS_CSV = os.path.join('data', 'reference', 'postcodes.csv')


def save_ref_csv(centroids):
    centroids[['pcds', 'oslaua', 'osward']].to_csv(
        CENTROIDS_CSV, index=False)


def load_input():
    return pd.read_csv('working/ref/postcodes.csv')


if __name__ == '__main__':
    data = load_input()
    save_ref_csv(data)
