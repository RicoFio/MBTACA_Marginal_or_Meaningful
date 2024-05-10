import geopandas as gpd
from pathlib import Path
import json
import time
import pandas as pd
from fuzzywuzzy import process, fuzz
from typing import List

STATIC_SITE_DATA_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/6.C85_FP/code/static/data"
)

PREPROCESSED_DATA_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/6.C85_FP/data/preprocessed_data"
)


def fuzzy_match(row, strings_to_match):
    zo_usede_str = str(row['zo_usede'])
    matches = process.extractOne(zo_usede_str,
                                 strings_to_match,
                                 scorer=fuzz.partial_ratio)
    return matches[1] > 90


def get_zoning_codes_for_type_for_municipality(
        zoning_atlas_data_for_municipality, strings_to_match: List[str]):
    matched_rows = zoning_atlas_data_for_municipality[
        zoning_atlas_data_for_municipality.apply(fuzzy_match,
                                                 axis=1,
                                                 args=(strings_to_match, ))]
    #these should be considered multifamily as the less exclusive zoning
    return matched_rows[
        'zo_abbr']  # the single family codes that do not include multifamily


def get_parcel_data_filtered_by_municipalities(municipalities):

    file_name = '_'.join(municipalities).lower()

    parcels_within_station_buffer = gpd.read_file(
        PREPROCESSED_DATA_PATH / 'station_only_parcels.geojson')
    selected_parcels = parcels_within_station_buffer[
        parcels_within_station_buffer["municipality"].isin(municipalities)]
    selected_parcels['zone_id'] = selected_parcels['zone_id'].apply(json.dumps)
    selected_parcels['routes'] = selected_parcels['routes'].apply(json.dumps)
    selected_parcels['route_colors'] = selected_parcels['route_colors'].apply(
        json.dumps)
    # write the brookline and milton parcels to a file so don't have to keep reading the big file in
    selected_parcels.to_file(PREPROCESSED_DATA_PATH /
                             f"{file_name}_parcels.geojson",
                             driver='GeoJSON')


def split_augmented_parcel_data_by_stop(filename):

    augmented_parcels_all_stops = gpd.read_file(
        STATIC_SITE_DATA_PATH /
        f"{filename}_parcels_for_upzone_willchange_viz.geojson")

    for stop_name in augmented_parcels_all_stops["stop_name"].unique():
        file_name = stop_name.lower().replace(' ', '_')

        df_for_stop = augmented_parcels_all_stops[
            augmented_parcels_all_stops["stop_name"] == stop_name]
        df_for_stop.to_file(
            STATIC_SITE_DATA_PATH /
            f"parcels/per_station/upzone_willchange_parcels_{file_name}.geojson",
            driver='GeoJSON')


def split_parcel_data_by_municipality():
    parcels_within_station_buffer = gpd.read_file(
        PREPROCESSED_DATA_PATH / 'station_only_parcels.geojson')

    print(
        f"processing {parcels_within_station_buffer['municipality'].nunique()} municipalities"
    )

    for municipality in parcels_within_station_buffer["municipality"].unique():

        file_name = municipality.lower().replace(' ', '_')

        parcels_for_municipality = parcels_within_station_buffer[
            parcels_within_station_buffer["municipality"] == municipality]

        selected_columns = [
            "municipality", "stop_name", 'USE_CODE', 'ZONING', "geometry"
        ]

        parcels_for_municipality = parcels_for_municipality[selected_columns]

        parcels_for_municipality.to_file(PREPROCESSED_DATA_PATH /
                                         f"{file_name}_parcels.geojson",
                                         driver='GeoJSON')
        print(f"wrote {file_name} file ")


# start = time.time()
# split_parcel_data_by_municipality()
# end = time.time()
# print('time elapsed', end - start)
