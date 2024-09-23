import json
import os
from pathlib import Path

# NOTE: this is a bit of WIP, getting more or less all the data we need for municipalities with data available but
# needs to be cleaned up and standardized.

LOCAL_PROJECT_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/MBTACA_Marginal_or_Meaningful/"
)

PER_STATION_DATA_PATH = LOCAL_PROJECT_PATH / "code/static/data/stop_zones/per_station/"

DATA_PATH = LOCAL_PROJECT_PATH / "data"
PREPROCESSED_DATA_PATH = DATA_PATH / "preprocessed_data"
STATIC_SITE_DATA_PATH = LOCAL_PROJECT_PATH / "code/static/data"


def get_filenames_in_directory(directory_path):
    filenames = [
        f
        for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f))
    ]
    return filenames


def count_features_in_geojson(file_path):
    # Open and load the GeoJSON file
    with open(file_path, "r") as f:
        geojson_data = json.load(f)

        # Get the 'features' array from the GeoJSON
        features = geojson_data.get("features", [])

        # Return the count of items in the features array
        return len(features)


def combine_geojson(files):
    # Initialize the combined GeoJSON structure

    output_file = (
        STATIC_SITE_DATA_PATH
        / "all_municipalities_stop_zone_zoning_usage_census.geojson"
    )
    combined_geojson = {"type": "FeatureCollection", "features": []}

    for file in files:
        with open(PER_STATION_DATA_PATH / file, "r") as f:
            geojson_data = json.load(f)
            # Append the features from the current file to the combined features list
            combined_geojson["features"].extend(geojson_data.get("features", []))

    # Write the combined GeoJSON to the output file
    with open(output_file, "w") as f:
        json.dump(combined_geojson, f, indent=4)


def transform_to_v2(combined_geojson):

    replace_fields = {
        "percentage_weighted_total_population_male": "weighted_pct_population_male",
        "percentage_weighted_total_population_female": "weighted_pct_population_female",
        "percentage_weighted_total_population_not_hispanic_or_latino": "weighted_pct_not_hispanic_latino",
        "percentage_weighted_total_population_not_hispanic_or_latino_white_alone": "weighted_pct_not_hispanic_latino_white",
        "percentage_weighted_total_population_not_hispanic_or_latino_black_or_african_american_alone": "weighted_pct_not_hispanic_latino_black",
        "percentage_weighted_total_population_not_hispanic_or_latino_american_indian_and_alaska_native_alone": "weighted_pct_not_hispanic_latino_native",
        "percentage_weighted_total_population_not_hispanic_or_latino_asian_alone": "weighted_pct_not_hispanic_latino_asian",
        "percentage_weighted_total_population_not_hispanic_or_latino_native_hawaiian_and_other_pacific_islander_alone": "weighted_pct_not_hispanic_latino_pi",
        "percentage_weighted_total_population_not_hispanic_or_latino_some_other_race_alone": "weighted_pct_not_hispanic_latino_other",
        "percentage_weighted_total_population_not_hispanic_or_latino_two_or_more_races": "weighted_pct_not_hispanic_latino_2+",
        "percentage_weighted_total_population_hispanic_or_latino": "weighted_pct_hispanic_latino",
        "weighted_median_household_income_in_2022_inflation_adjusted_dollars": "weighted_median_hh_income",
        "percentage_weighted_workers_16_years_and_over_car_truck_or_van": "pct_workers_car_van",
        "percentage_weighted_workers_16_years_and_over_drove_alone": "pct_workers_drive_alone",
        "percentage_weighted_workers_16_years_and_over_public_transportation_includes_taxicab": "pct_workers_public_transportation",
        "percentage_weighted_workers_16_years_and_over_motorcycle": "pct_workers_motorcycle",
        "percentage_weighted_workers_16_years_and_over_bicycle": "pct_workers_bicycle",
        "percentage_weighted_workers_16_years_and_over_walked": "pct_workers_walked",
        "percentage_weighted_workers_16_years_and_over_other_means": "pct_workers_other",
        "percentage_weighted_workers_16_years_and_over_worked_at_home": "pct_workers_wfh",
        "percentage_weighted_occupied_housing_units_no_vehicle_available": "pct_hh_0_vehs",
        "percentage_weighted_occupied_housing_units_1_vehicle_available": "pct_hh_1_vehs",
        "percentage_weighted_occupied_housing_units_2_vehicle_available": "pct_hh_2_vehs",
    }

    v2_fields = [
        "stop_name",
        "weighted_total_population",
        "weighted_total_population_density_permile",
        "weighted_total_population_male",
        "weighted_total_population_female",
        "weighted_pct_population_male",
        "weighted_pct_population_female",
        "weighted_pct_not_hispanic_latino",
        "weighted_pct_not_hispanic_latino_white",
        "weighted_pct_not_hispanic_latino_black",
        "weighted_pct_not_hispanic_latino_native",
        "weighted_pct_not_hispanic_latino_asian",
        "weighted_pct_not_hispanic_latino_pi",
        "weighted_pct_not_hispanic_latino_other",
        "weighted_pct_not_hispanic_latino_2+",
        "weighted_pct_hispanic_latino",
        "weighted_pct_hispanic_latino_white",
        "weighted_pct_hispanic_latino_black",
        "weighted_pct_hispanic_latino_native",
        "weighted_pct_hispanic_latino_asian",
        "weighted_pct_hispanic_latino_pi",
        "weighted_pct_hispanic_latino_other",
        "weighted_pct_hispanic_latino_2+",
        "weighted_median_hh_income",
        "pct_workers_car_van",
        "pct_workers_drive_alone",
        "pct_workers_drive_carpooled",
        "pct_workers_public_transportation",
        "pct_workers_motorcycle",
        "pct_workers_bicycle",
        "pct_workers_walked",
        "pct_workers_other",
        "pct_workers_wfh",
        "pct_hh_0_vehs",
        "pct_hh_1_vehs",
        "municipality",
        "pctZonedAsSF",
        "isZonedAsCommercial",
        "pctZonedAsMultifamily",
        "pctUsedAsSF",
        "pctUsedAsCommercial",
        "pctUsedAsDuplex",
        "pctUsedAsTriplex",
        "pctUsedAsMultiBuildings1Lot",
        "pctUsedAsAptUpTo30Units",
        "pctUsedAsAptOver30Units",
        "pctUsedAsCoopApt",
        "pctUsedAsOtherMultifamily",
        "pctMustUpzone",
        "pctWillChange",
        "pctFutureZonedAsSF",
        "pctFutureZonedAsMulti",
    ]

    output_data = {"type": "FeatureCollection", "features": []}

    for feature in combined_geojson["features"]:

        feature_renamed = {
            replace_fields[k] if k in replace_fields else k: v
            for k, v in feature["properties"].items()
        }

        # TODO: this is a bit of a hack, not sure why the total population isn't in there.
        feature_renamed["weighted_total_population"] = (
            feature_renamed["weighted_total_population_male"]
            + feature_renamed["weighted_total_population_female"]
        )

        feature_renamed["weighted_total_population_density_permile"] = (
            feature_renamed["weighted_total_population"] / feature_renamed["sq_miles"]
        )

        # put the new renamed properties dict into the old feature
        feature["properties"] = feature_renamed

        # Create a new feature_renamed with filtered properties
        filtered_properties = {
            key: feature["properties"][key]
            for key in v2_fields
            if key in feature["properties"]
        }

        # TODO: some of these features need to be renamed, need some sort of mapping.
        new_feature = {
            "type": feature["type"],
            "properties": filtered_properties,
            "geometry": feature["geometry"],
        }

        output_data["features"].append(new_feature)

    output_file = (
        STATIC_SITE_DATA_PATH
        / "all_municipalities_stop_zone_zoning_usage_census_v2.geojson"
    )

    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=4)

    print(f"wrote v2 data to file: {output_file}")

    # json.dumps(output_data, indent=2)


if __name__ == "__main__":
    geojson_files = get_filenames_in_directory(PER_STATION_DATA_PATH)
    print("num files", len(geojson_files))

    combine_geojson(geojson_files)
    with open(
        STATIC_SITE_DATA_PATH
        / "all_municipalities_stop_zone_zoning_usage_census.geojson",
        "r",
    ) as f:
        all_stops = json.load(f)
    transform_to_v2(all_stops)

    print("Combined GeoJSON saved")


# problem is potentially the zoning codes on several of the municipalities
