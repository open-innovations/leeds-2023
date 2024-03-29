import os
import pandas as pd
import datetime

PATH_EXCEL = os.path.join("working", "Leeds 2023 AVE.xlsx")
OUTPUT_PATH = os.path.join("data", "metrics", "media_coverage")
RAW_CSV = os.path.join(OUTPUT_PATH, "raw_data.csv")

SITE_DATA_PATH = os.path.join("docs", "_data", "metrics", "media_coverage")

def read_media_metrics(sheet_name='Aug 2021 - July 2022'):
    media_data = pd.read_excel(PATH_EXCEL, sheet_name=sheet_name, usecols=range(0, 10), thousands=',', na_values=['N/A '])

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

    media_data['CIRC'] = media_data.CIRC.fillna(0).astype(int)

    # Clean up names
    media_data.columns = media_data.columns.str.strip()

    kpi = media_data.groupby(['Scope', 'Type', 'Month'], as_index=False).size()

    kpi = kpi.pivot(index=["Scope", "Type"], columns="Month", values="size")
    kpi = kpi.fillna(0)
    kpi['Total'] = kpi.sum(axis=1)
    for col in list(kpi):
        kpi[col] = kpi[col].astype("Int64")

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    kpi.to_csv(os.path.join(OUTPUT_PATH, "coverage_report.csv"))
    media_data.to_csv(RAW_CSV, index=False)


def load_raw_data(cols=None):
    '''Load raw data from CSV. Optionally specify columns.'''
    data = pd.read_csv(RAW_CSV, usecols=cols, parse_dates=["Date"])
    return data


def media_summary(data):
    summary = pd.DataFrame({
      'count': data.Subject.count(),
      'cumulative_count': data.Subject.count().cumsum(),
      'reach': data.CIRC.sum(),
      'cumulative_reach': data.CIRC.sum().cumsum(),
    })
    return summary


def filter_coverage_by_period(earliest, latest):
    raw = load_raw_data(cols=['Date', 'Subject', 'CIRC', 'Month'])
    filtered = raw[ (raw.Date >= earliest) & (raw.Date < latest) ]
    return filtered


def summarise():
    data = load_raw_data(cols=['Date', 'Subject', 'CIRC'])

    data['Period'] = data.Date.dt.to_period('A-JUL')
    annual = data.groupby('Period')

    summary = media_summary(annual)
    os.makedirs(SITE_DATA_PATH, exist_ok=True)
    summary.to_csv(os.path.join(SITE_DATA_PATH, 'summary.csv'))

    # Prepare paths for KPI reports
    KPI_REPORT_PATH = os.path.join(SITE_DATA_PATH, 'kpi')
    os.makedirs(KPI_REPORT_PATH, exist_ok=True)

    # Prep data for LCC 2021 report
    lcc_21_22 = media_summary(
      filter_coverage_by_period(
        earliest = datetime.datetime.fromisoformat('2021-04-01'),
        latest = datetime.datetime.fromisoformat('2022-04-01')
      ).groupby('Month')
    )
    lcc_21_22.to_csv(os.path.join(KPI_REPORT_PATH, 'lcc_21_22.csv'))

    # Prep data for LCC 2022-24 report
    lcc_22_24 = media_summary(
      filter_coverage_by_period(
        earliest = datetime.datetime.fromisoformat('2022-04-01'),
        latest = datetime.datetime.fromisoformat('2024-04-01')
      ).groupby('Month')
    )
    lcc_22_24.to_csv(os.path.join(KPI_REPORT_PATH, 'lcc_22_24.csv'))


def main():
    read_media_metrics()


if __name__ == '__main__':
    main()
