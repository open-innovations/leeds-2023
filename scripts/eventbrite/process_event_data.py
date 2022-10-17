import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def df_to_gdf(input_df):
    df = input_df.copy()
    geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    return gpd.GeoDataFrame(df, geometry=geometry)


output_data = (
pd.read_csv("data\metrics\eventbrite\leeds_2023_events.csv")
  .filter(["name.text","venue.longitude","venue.latitude","start.utc"])
  .rename({"name.text":"Name","venue.longitude":"longitude","venue.latitude":"latitude","start.utc":"Start Time"},axis="columns")
  .pipe(df_to_gdf) 
  .to_json()     
)

OUTPUT_FP = "data\\metrics\\eventbrite\\test.geojson"
with open(OUTPUT_FP, 'w') as geojson_file:
        geojson_file.write(output_data)


