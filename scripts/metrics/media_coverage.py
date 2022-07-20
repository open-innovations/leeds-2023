import os
import pandas as pd

PATH_EXCEL = os.path.join("working", "Leeds 2023 AVE.xlsx")
OUTPUT_PATH = os.path.join("data", "metrics", "media_coverage")
RAW_CSV = os.path.join(OUTPUT_PATH, "raw_data.csv")

SITE_DATA_PATH = os.path.join("docs", "_data", "metrics", "media_coverage")

def read_media_metrics(sheet_name='Aug 2021 - July 2022'):
    media_data = pd.read_excel(PATH_EXCEL, sheet_name=sheet_name, usecols=range(0, 10))

    # data9[~data9[data9.columns[1]].isna()].reset_index(drop=True)
    media_data = media_data[~media_data['Publication'].isna()]

    media_data = media_data.rename(columns={
        "Feature, News, Mention, Opinion / Comment": "Type",
        "Trade, National, Regional, Local, Int'tional": "Scope"
    })

    media_data["Date"] = pd.to_datetime(media_data["Date"], format="%d.%m.%y")
    media_data["Month"] = media_data["Date"].dt.to_period("M")

    media_data["Scope"] = media_data["Scope"].str.strip().str.lower()
    media_data["Scope"] = media_data["Scope"].replace(
      to_replace={
        "national": "national/trade",
        "trade": "national/trade",
      }
    )

    media_data["Type"] = media_data["Type"].str.strip().str.lower()
    media_data["Type"] = media_data["Type"].replace(
      to_replace={
        "comment": "comment/opinion",
        "opinion": "comment/opinion",
      }
    )

    media_data["Month"] = media_data["Month"].fillna("N/A")

    kpi = media_data.groupby(['Scope', 'Type', 'Month'], as_index=False).size()

    kpi = kpi.pivot(index=["Scope", "Type"], columns="Month", values="size")
    kpi = kpi.fillna(0)
    kpi['Total'] = kpi.sum(axis=1)
    for col in list(kpi):
        kpi[col] = kpi[col].astype("Int64")

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    kpi.to_csv(os.path.join(OUTPUT_PATH, "coverage_report.csv"))
    media_data.to_csv(RAW_CSV, index=False)


def summarise():
    data = pd.read_csv(RAW_CSV, parse_dates=["Date", "Month"])

    data['Year'] = data.Date.dt.to_period('A-JUL')

    summary = data.groupby('Year').count()[["Subject "]]
    summary = summary.rename(columns = {
      "Subject ": "Count"
    })
    
    os.makedirs(SITE_DATA_PATH, exist_ok=True)
    summary.to_csv(os.path.join(SITE_DATA_PATH, 'summary.csv'))

def main():
    read_media_metrics()


if __name__ == '__main__':
    main()
