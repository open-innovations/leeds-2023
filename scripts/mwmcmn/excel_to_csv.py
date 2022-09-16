import pandas as pd
import numpy as np


def main(in_args,out_args):
    df = pd.read_excel(**in_args)
    df.to_csv(**out_args)

in_args = { "io" : "data\\reference\MWMCMN 60622 ACE Global Data.xlsx",
            "sheet_name" : "GLOBAL QUANT",
            "skiprows" : 4,
            "nrows" : 23,
            "usecols" : "A:I",
            }

out_args = { "path_or_buf" : "data\\reference\mwmcmn_projects__test.csv",
              "index" : False
            }

main(in_args,out_args)

