import pandas as pd
import yaml
import sys
import os

def first(data,column):
    return list(data[column])[0]

def last(data,column):
    return list(data[column])[-1]

def difference(data,column):
    return last(data,column) - first(data,column)

def col_max(data,column):
    return max(data[column])

def col_min(data,column):
    return min(data[column])

def col_range(data,column):
    return col_max(data,column) - col_min(data,column)

def total(data,column):
    return sum(data[column])

def count(data,column):
    return len(data[column])

def average(data,column):
    return (sum(data[column]) / len(data[column]))

def average_int(data,column):
    return (int)(sum(data[column]) / len(data[column]))

stats = {
    "first" : first,
    "last" : last,
    "difference" : difference,
    "max" : col_max,
    "min" : col_min,
    "range" : col_range,
    "count" : count,
    "total" : total,
    "average" : average_int
}

#reserved-tl: data-file,data-files-label
#reserved-fl: metrics,path,group-by-date

def get_metric(data,metric_labels):
    column,stat = metric_labels.rsplit("_",1)
    return stats[stat](data,column)

def get_metrics(data,metric_labels):
    return {m : get_metric(data,m) for m in metric_labels}

def add_top_level_meta(tl_meta,summarys,keep_label=False):
    label = tl_meta.get("data_files_label","data")
    tl = tl_meta | { "data_file" : summarys}
    tl[label] = tl.pop("data_file")
    if not keep_label:
        tl.pop("data_files_label")

    return tl

def add_file_level_meta(file_meta,summary,keep_reserved=False):
    fl = file_meta | {"metrics" : summary}

    if not keep_reserved:
        [fl.pop(key,"") for key in ["path","group_by_date"]]

    return fl

def filter_data(data: pd.DataFrame,filter_col,filter_range):
    min,max = filter_range.split(":")
    data = data[data[filter_col] >= min]
    data = data[data[filter_col] <= max]
    return data


def get_summary_file(config):
    data = pd.read_csv(config["path"])
    data = filter_data(data,config["filter_col"],config["filter_range"])
    metrics = get_metrics(data,config["metrics"])
    return metrics #format(metrics)


def get_summary_dir(config):
    summary = []
    for file in os.listdir(config["path"]):
        summary.append({"key" : file.replace(".csv","")} | get_summary_file(config | {"path" : config["path"] + file}))
 
    return summary

def get_summary_file_group_by_date(config):
    summary = []
    data = pd.read_csv(config["path"])
    data = filter_data(data,config["filter_col"],config["filter_range"])
    column,period = config["group_by_date"].split("_")
    
    data[column] = pd.to_datetime(data[column])
    data["period"] = data[column].dt.to_period(period)
    col_name = config["group_by_date_col"] if "group_by_date_col" in config.keys() else "key"
    for p in data["period"].unique():
        filtered_data = data[data[column].dt.to_period(period) == p]
        metrics = {col_name : str(p).split("/")[0]} | get_metrics(filtered_data,config["metrics"])
        summary.append(metrics)

    
    return summary

def get_summarys(input):
    summarys = {}
    for file_key in input["data_file"].keys():
        config = input["data_file"][file_key]
        if os.path.isfile(config["path"]):
            if "group_by_date" in config.keys():
                data =  get_summary_file_group_by_date(config)
                pd.json_normalize(data).to_csv(config["out_csv"],index=False)
                summarys[file_key] =  {}
                #summarys[file_key] =  get_summary_file_group_by_date(config)                
            else:
                summarys[file_key] =  get_summary_file(config)
        else:
            summarys[file_key] =  get_summary_dir(config)

        summarys[file_key] = add_file_level_meta(config,summarys[file_key])

    return add_top_level_meta(input,summarys)


def write_yaml(path,data):
    with open(path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, sort_keys=False)

def read_yaml(path):
    with open(path, 'r') as infile:
        return yaml.safe_load(infile)

def summary_yaml(input_path):
    return get_summarys(read_yaml(input_path))
    
    
def summary_write_yaml(input_path,output_path):
    write_yaml(output_path,summary_yaml(input_path))

if(__name__ == "__main__"):
    yaml_path_in = sys.argv[1]  
    yaml_path_out = sys.argv[2] 
    summary_write_yaml(yaml_path_in,yaml_path_out)
    