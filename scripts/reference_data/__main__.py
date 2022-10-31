import argparse
from postcodes import get_leeds_postcode_centroids
import logging


def parse_opts():
    parser = argparse.ArgumentParser(prog="reference_data",
                                     description='LEEDS 2023 Reference Data updater')
    parser.add_argument('-f', '--force', action='store_true',
                        help='force re-processing of files')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    opts = parse_opts()
    get_leeds_postcode_centroids(force=opts.force)
