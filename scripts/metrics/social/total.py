import combine

DATA_DIR = "docs\\_data\\metrics\\social_media\\service"
OUT = "docs\\_data\\metrics\\social_media\\all_weekly.csv"
all = combine.combine_dir(DATA_DIR).groupby(by="week_starting").sum()
print(all)
all.to_csv(OUT,index=True)