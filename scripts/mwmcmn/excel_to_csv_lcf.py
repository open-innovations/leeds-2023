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
  df["Benefited_Total"] = df["Benefited_0_4"] + df["Benefited_5_12"] + df["Benefited_13_18"] + df["Benefited_19_25"] + df["Benefited_Unknown"]
  return df
   
def main(in_args,out_args):
    df = pd.read_excel(**in_args)
    df = clean(df)
    df.to_csv(**out_args)

read_args = { "io" : "working\\mwmcmn\\MWMCMN 060622 LCF Data.xlsx",
            "sheet_name" : "Sheet1",
            "header" : 5,
            "skiprows" : range(6,7),
            "nrows" : 22,
            "usecols" : "C:N,P:T",
            "names" : ["Benefited_Total","Benefited_0_4","Benefited_5_12","Benefited_13_18","Benefited_19_25","Benefited_Unknown","Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10","Q11"]
            }

write_args = { "path_or_buf" : "data\\reference\\mwmcmn\\mwmcmn_lcf.csv",
              "index" : True   
             }

main(read_args,write_args)

