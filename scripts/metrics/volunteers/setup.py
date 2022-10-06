import logging
import os

DATA_DIR = os.path.join('data', 'metrics', 'volunteers')
VIEW_DIR = os.path.join('docs', '_data', 'metrics', 'volunteers')


def setup_folders():
    logging.info('Setting up directories')
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(VIEW_DIR, exist_ok=True)
