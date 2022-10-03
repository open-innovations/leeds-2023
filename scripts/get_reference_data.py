import os
import pandas as pd
import geopandas as gpd
import urllib.request


def get_leeds_postcode_centroids():
    '''
    Get the latest ONS Postcode Database from the ONS.

    https://www.ons.gov.uk/methodology/geography/geographicalproducts/postcodeproducts
    '''
    SOURCE_CSV = os.path.join('working', 'ONSPD_AUG_2022_UK.csv')
    PARQUET_FILE = os.path.join('working', 'centroids.parquet')
    CENTROIDS_CSV = os.path.join('data', 'reference', 'postcodes.csv')
    CENTROIDS_JSON = os.path.join('data', 'reference', 'postcodes.geojson')

    if not os.path.exists(SOURCE_CSV):
        raise "Can't find source CSV {0}. Have you downloaded it?".format(SOURCE_CSV)

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
