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
  df["YP_Benefited_Total"] = df["YP_Benefited_0_4"] + df["YP_Benefited_5_12"] + df["YP_Benefited_13_18"] + df["YP_Benefited_19_25"] + df["YP_Benefited_Unknown"]
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
            "names" : ["YP_Benefited_Total","YP_Benefited_0_4","YP_Benefited_5_12","YP_Benefited_13_18","YP_Benefited_19_25","YP_Benefited_Unknown","YP_First_Time_Participation","YP_Previous_Barriers","YP_Increased_Cultural_Awareness","YP_Positive_Experience","YP_Self_Expression","YP_Continued_Engagement","Improved_Social_Networks","Increased_Belonging_Community","Community_Volunteers_Supporters","Improved_Mental_Health","Improved_Physcial_Health"]
            }

write_args = { "path_or_buf" : "data\\reference\\mwmcmn\\mwmcmn_lcf.csv",
              "index" : True   
             }

main(read_args,write_args)

