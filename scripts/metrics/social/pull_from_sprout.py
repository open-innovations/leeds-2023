import pandas as pd
import combine
import clean
import os

def clear_dir(dir: str):
    for file in combine.dir_file_paths(dir):
        os.remove(file)

def main():
    TEMP_DIR_LOCATION = os.path.join('working','sprout')
    MASTER_FILE_LOCATION = os.path.join('data','metrics','social')
    MASTER_FILE_NAME_TEMP = '{}.csv'

    df =  combine.combine_dir(TEMP_DIR_LOCATION)
    split = df.groupby("Network")
    dfs = {table.lower() : split.get_group(table) for table in list(split.groups.keys())}

#TODO new data should take priority over master file
    for key in dfs:
        master_file_path = os.path.join(MASTER_FILE_LOCATION,MASTER_FILE_NAME_TEMP.format(key))
        combine.combine_file_df(master_file_path,dfs[key],pre=clean.clean_df_1,post=clean.clean_df_2,write_path=master_file_path)

if(__name__ == "__main__"):
    main()
#Use if nothing in data files
#for key in dfs:
#    master_file_path = MASTER_FILE_LOCATION.format(key)
#    combine.combine_dfs([dfs[key]],pre=clean.clean_df_1,post=clean.clean_df_2,write_path=master_file_path)

#clear_dir(TEMP_DIR_LOCATION)
