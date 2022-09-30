import pandas as pd
import os
import sys

def removePercentSigns(data):   
    for col in list(data.columns[1:]):
        data[col] = data[col].astype('string').str.replace("%","").astype(data[col].dtype)

def makeFloatNullableInt(data):
    for col in list(data.columns[1:]):
        if data[col].dtype == "float64":
            if floatContainsIntsOnly(data[col]):
                data[col] = data[col].astype("Int64")

def floatContainsIntsOnly(column) -> bool:
    for f in list(column):
        if not f.is_integer():
            return False

    return True

def rename_cols(df: pd.DataFrame):
    df.columns = [c.replace("(","").lower() for c in df.columns]
    df.columns = [c.replace(")","").lower() for c in df.columns]
    df.columns = [c.replace(" ","_").lower() for c in df.columns]

def drop_cols(df: pd.DataFrame,to_drop: list[str]) -> pd.DataFrame:
    return df.drop(columns=to_drop,errors="ignore")

def sort_df(df: pd.DataFrame, sort_col: str) -> pd.DataFrame:
    df = df.sort_values(sort_col)
    return df

DROP = ["network","profile"]
DATE_FORMAT_IN = '%m-%d-%Y'
DATE_FORMAT_OUT = '%Y-%m-%d'
            
def clean_df_1(df: pd.DataFrame) -> pd.DataFrame:
    df  = df.dropna(axis="columns",how="all")
    df = df.fillna(0)
    rename_cols(df)
    df = drop_cols(df,DROP)
    removePercentSigns(df)
    makeFloatNullableInt(df)
    df = df.replace(',','', regex=True)
    df.date = pd.to_datetime(df.date,format=DATE_FORMAT_IN,errors="ignore").dt.strftime(DATE_FORMAT_OUT)

    return df

SORT = "date"
def clean_df_2(df: pd.DataFrame) -> pd.DataFrame:
    df = df.fillna(0)
    makeFloatNullableInt(df)
    df = df.drop_duplicates(subset=SORT,keep="last")
    df = sort_df(df,SORT)
    return df



