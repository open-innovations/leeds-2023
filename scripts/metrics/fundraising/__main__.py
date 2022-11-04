import sys

from lib import copy_to_site, process
import metrics.fundraising.progress

def process_orgs_from_goodcrm(file):
    process(file)
    copy_to_site()


if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = 'working/fundraising_orgs.csv'
    # process_orgs_from_goodcrm(file)


    metrics.fundraising.progress.process()
