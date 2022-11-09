import os
import sys
import pandas as pd
import logging

logger = logging.getLogger(__name__)

CENTROIDS_CSV = os.path.join('data', 'reference', 'postcodes.csv')


def save_ref_csv(centroids):
    centroids[['pcds', 'oslaua', 'osward']].to_csv(
        CENTROIDS_CSV, index=False)


def load_input(input_file):
    return pd.read_csv(input_file)


if __name__ == '__main__':
    input_file = sys.argv[1]
    data = load_input(input_file)
    save_ref_csv(data)
