import logging
import os

WORKING_DIR = os.path.join('working', 'metrics', 'rosterfy')
DATA_DIR = os.path.join('data', 'metrics', 'volunteers')
VIEW_DIR = os.path.join('docs', 'metrics', 'volunteers', '_data')
META_DIR = os.path.join(VIEW_DIR, 'metadata')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VIEW_DIR, exist_ok=True)


def setup_folders():
    logging.info('Setting up directories')
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(VIEW_DIR, exist_ok=True)
