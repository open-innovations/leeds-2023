from cmath import isnan
import pandas as pd

def floatContainsIntsOnly(column) -> bool:
  for f in list(column):
    if not (f.is_integer() or isnan(f)):
      return False

  return True

def makeFloatNullableInt(df:pd.DataFrame) -> pd.DataFrame:
  #print(df.col)
  for col in list(df.columns):
    if df[col].dtype == "float64":          
      if floatContainsIntsOnly(df[col]):
        df[col] = df[col].astype("Int32")

  return df
                
def clean(df: pd.DataFrame):
  df.index.name = "Artist_ID"
  df = makeFloatNullableInt(df)
  return df
  
def main(in_args,out_args):
    df = pd.read_excel(**in_args)
    df = clean(df)
    df.to_csv(**out_args)

read_args = { "io" : "working\\mwmcmn\\MWMCMN 60622 ACE Global Data.xlsx",
            "sheet_name" : "GLOBAL QUANT",
            "header" : 4,
            "skiprows" : range(5,6),
            "nrows" : 22,
            "usecols" : "B:I",
            "names" : ["Sponsored_Artists_Days_Testing","Other_Artists_Employed_Days","Performance_Or_Exhibition_Days","Sessions_For_Education_Training_Or_Participation","Artists_Employed","Participants","Live_Audience","Online_Audience"]
            }

write_args = { "path_or_buf" : "data\\reference\\mwmcmn\\mwmcmn_ace.csv",
              "index" : True
            }

main(read_args,write_args)

