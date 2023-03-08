import os

ROOTDIR=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def resolve_path(path):
    return os.path.join(ROOTDIR, path)