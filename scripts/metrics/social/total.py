import combine
import yaml
import os

SUMMARY_DIR = os.path.join('docs','_data','metrics','social_media','summary.yml')
DATA_DIR = os.path.join('docs','_data','metrics','social_media','service')
os.makedirs(DATA_DIR, exist_ok=True)

def summary_total():
    socials = ['twitter','instagram','facebook','linkedin']
    metrics = ['audience_last','engagements_total','audience_gained_total','impressions_total']

    with open(SUMMARY_DIR,'r') as f:
        stats = yaml.safe_load(f)
    stats['service'] = stats['service'] | {'all' : {'metrics' : {}} }
    for metric in metrics:
        stats['service']['all']['metrics'][metric] = sum([stats['service'][social]['metrics'][metric] for social in socials])

    with open(SUMMARY_DIR,'w') as f:
        yaml.safe_dump(stats,f)

def main():
    OUT = os.path.join('docs','_data','metrics','social_media','all_weekly.csv')
    all = combine.combine_dir(DATA_DIR).groupby(by="week_ending").sum()
    all.to_csv(OUT,index=True)
    summary_total()

if(__name__ == "__main__"):
    main()