import sys

from lib import copy_to_site, process

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = 'working/fundraising_orgs.csv'
    process(file)
    copy_to_site()
