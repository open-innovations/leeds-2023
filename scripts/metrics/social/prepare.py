import total
import get_stats
import os

TOTAL_PATH_CONFIG = os.path.join('scripts','metrics','social','total_summary_config.yml')
WEEKLY_PATH_CONFIG = os.path.join('scripts','metrics','social','weekly_summary_config.yml')

TOTAL_PATH_OUT = os.path.join('docs','metrics','social-media','_data','headlines.yml')
WEEKLY_PATH_OUT = os.path.join('working','junk.yml')


def main():
    get_stats.summary_write_yaml(TOTAL_PATH_CONFIG,TOTAL_PATH_OUT)
    get_stats.summary_write_yaml(WEEKLY_PATH_CONFIG,WEEKLY_PATH_OUT)
    total.main()
    
if(__name__ == "__main__"):
    main()