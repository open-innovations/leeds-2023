import pull_from_sprout
import total
import get_stats

def main():
    pull_from_sprout.main()
    get_stats.summary_write_yaml("scripts\\metrics\\social\\total_summary_config.yml","docs\_data\metrics\social_media\summary.yml")
    get_stats.summary_write_yaml("scripts\\metrics\\social\\weekly_summary_config.yml","working\junk.yml")
    total.main()
    
if(__name__ == "__main__"):
    main()