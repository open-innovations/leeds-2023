import os
import pandas as pd
import geopandas as gpd
import urllib.request


def get_leeds_postcode_centroids():
    '''
    Download postcode centroids

    Homepage: https://data.gov.uk/dataset/6de48d19-b3a0-4e45-b98e-01bd781b035c/ons-postcode-directory-latest-centroids
    '''
    CENTROIDS_URL = 'http://geoportal.statistics.gov.uk/datasets/75edec484c5d49bcadd4893c0ebca0ff_0.csv'
    SOURCE_CSV = os.path.join('working', 'centroids.csv')
    PARQUET_FILE = os.path.join('working', 'centroids.parquet')
    CENTROIDS_CSV = os.path.join('data', 'reference', 'postcodes.csv')
    CENTROIDS_JSON = os.path.join('data', 'reference', 'postcodes.geojson')

    if not os.path.exists(SOURCE_CSV):
        with urllib.request.urlopen(CENTROIDS_URL) as r:
            with open(SOURCE_CSV, 'wb') as f:
                f.write(r.read())

    columns = 'pcds lat long pcon osward lsoa11 msoa11'.split()
    if not os.path.exists(PARQUET_FILE):
        centroids = pd.read_csv(SOURCE_CSV, usecols=columns)
        bbox = [-1.900634, 53.569676, -1.251068, 53.962549]
        centroids = centroids[(centroids.long >= bbox[0]) & (centroids.lat >= bbox[1]) & (centroids.long <= bbox[2]) & (centroids.lat <= bbox[3])]

        centroids = gpd.GeoDataFrame(
            centroids, geometry=gpd.points_from_xy(
                centroids.long, centroids.lat)
        )
        centroids.to_parquet(PARQUET_FILE)
    else:
        centroids = gpd.read_parquet(PARQUET_FILE)

    centroids.to_csv(CENTROIDS_CSV, index=False, columns=columns)


get_leeds_postcode_centroids()
