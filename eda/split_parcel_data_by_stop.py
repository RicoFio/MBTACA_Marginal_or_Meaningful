import geopandas as gpd
from pathlib import Path

STATIC_SITE_DATA_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/6.C85_FP/code/static/data"
)

augmented_parcels_all_stops = gpd.read_file(
    STATIC_SITE_DATA_PATH /
    f"brookline_milton_parcels_for_upzone_willchange_viz.geojson")


for stop_name in augmented_parcels_all_stops["stop_name"].unique():
    file_name = stop_name.lower().replace(' ', '_')

    df_for_stop = augmented_parcels_all_stops[
        augmented_parcels_all_stops["stop_name"] == stop_name]
    df_for_stop.to_file(
        STATIC_SITE_DATA_PATH /
        f"parcels/per_station/upzone_willchange_parcels_{file_name}.geojson",
        driver='GeoJSON')
