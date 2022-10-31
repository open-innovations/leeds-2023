import os
import pandas as pd
import geopandas as gpd
import logging

logger = logging.getLogger(__name__)

SOURCE_CSV = os.path.join('working', 'ONSPD_AUG_2022_UK.csv')
PARQUET_FILE = os.path.join('working', 'centroids.parquet')
CENTROIDS_CSV = os.path.join('data', 'reference', 'postcodes.csv')
CENTROIDS_JSON = os.path.join('data', 'reference', 'postcodes.geojson')


def get_centroids(force=False):
    '''
    Get the latest ONS Postcode Database from the ONS.

    https://www.ons.gov.uk/methodology/geography/geographicalproducts/postcodeproducts
    '''

    if not os.path.exists(SOURCE_CSV):
        logger.error('Cannot find source CSV')
        raise "Can't find source CSV {0}. Have you downloaded it?".format(
            SOURCE_CSV)

    """
      pcds       Postcode (variable length with spaces)
      lat, long  Centroid of postcode - lat/long
      pcon       Westminster parliamentary constituency
      oslaua     Local authority district (LAD)/unitary authority (UA)/ metropolitan district (MD)/ London borough (LB)/ council area (CA)/district council area (DCA)
      osward     (Electoral) ward/division
      lsoa11     2011 Census Lower Layer Super Output Area (LSOA)/ Data Zone (DZ)/ SOA
      msoa11     2011 Census Middle Layer Super Output Area (MSOA)/ Intermediate Zone (IZ)
    """
    columns = 'pcds lat long pcon oslaua osward lsoa11 msoa11'.split()
    if force or not os.path.exists(PARQUET_FILE):
        logger.info('Processing CSV to Parquet')
        centroids = pd.read_csv(SOURCE_CSV, usecols=columns)
        # bbox = [-2.36, 53.26, -0.67, 54.15]
        # centroids = centroids[(centroids.long >= bbox[0]) & (centroids.lat >= bbox[1]) & (
        #     centroids.long <= bbox[2]) & (centroids.lat <= bbox[3])]

        centroids.to_parquet(PARQUET_FILE)
    else:
        logger.info('Reading existing Parquet file')
        centroids = pd.read_parquet(PARQUET_FILE)

    return centroids


def create_geographic_files():
    # Round numeric values to 5 decimal places
    centroids = centroids.round({'lat': 5, 'long': 5})
    centroids = gpd.GeoDataFrame(
        centroids, geometry=gpd.points_from_xy(
            centroids.long, centroids.lat)
    )


def save_ref_csv(centroids):
    centroids[['pcds', 'oslaua', 'osward']].to_csv(
        CENTROIDS_CSV, index=False)


def process(force=False):
    centroids = get_centroids(force=force)
    save_ref_csv(centroids)
