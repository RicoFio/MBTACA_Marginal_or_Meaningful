import geopandas as gpd
from pathlib import Path
import pandas as pd
import time
import data_generation_helpers as helpers
from fiona.errors import FionaValueError
import os

LOCAL_PROJECT_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/MBTACA_Marginal_or_Meaningful/"
)

DATA_PATH = LOCAL_PROJECT_PATH / "data"
PREPROCESSED_DATA_PATH = DATA_PATH / "preprocessed_data"
STATIC_SITE_DATA_PATH = LOCAL_PROJECT_PATH / "code/static/data"


def assign_zoning_by_parcel(
    zoning_atlas_for_municipality: str, parcel_data_for_municipality: pd.DataFrame
) -> pd.DataFrame:

    sf_zoning_codes = helpers.get_zoning_codes_for_type_for_municipality(
        zoning_atlas_for_municipality, ["Single", "One"]
    )
    multifamily_zoning_codes = helpers.get_zoning_codes_for_type_for_municipality(
        zoning_atlas_for_municipality, ["Multi Family", "Multiple Family", "Two Family"]
    )
    commercial_zoning_codes = helpers.get_zoning_codes_for_type_for_municipality(
        zoning_atlas_for_municipality, ["Commercial"]
    )

    sf_zoning_codes = list(
        set(sf_zoning_codes) - set(multifamily_zoning_codes)
    )  # the single family codes that do not include multifamily. some codes encompass multi and single and these should be considered multifamily for this analysis

    commercial_zoning_codes = list(
        set(commercial_zoning_codes) - set(multifamily_zoning_codes)
    )  # similarly, decide that areas that are both multifamily and commercial are just multifamily

    parcel_data_for_municipality["isZonedAsSF"] = parcel_data_for_municipality[
        "ZONING"
    ].apply(lambda zoning_code: zoning_code in sf_zoning_codes)
    parcel_data_for_municipality["isZonedAsMultifamily"] = parcel_data_for_municipality[
        "ZONING"
    ].apply(lambda zoning_code: zoning_code in multifamily_zoning_codes)
    parcel_data_for_municipality["isZonedAsCommercial"] = parcel_data_for_municipality[
        "ZONING"
    ].apply(lambda zoning_code: zoning_code in commercial_zoning_codes)

    return parcel_data_for_municipality


def assign_usage_by_parcel(parcel_data: pd.DataFrame) -> pd.DataFrame:

    # Assign usage by parcel
    # these are for all of Massachusetts: https://www.cityofboston.gov/images_documents/ma_occcodes_tcm3-16189.pdf
    single_family_usage_codes = ["101"]
    commercial_use_codes = [str(num) for num in range(310, 399 + 1)]  # remove parking?
    duplex_use_codes = ["104"]
    triplex_use_codes = ["105"]
    multi_buildings_1lot_use_codes = ["109"]
    apt_up_to_30_units_use_codes = ["111", "112"]
    apt_over_30_units_use_codes = ["113", "114"]
    coop_apt_use_codes = ["115"]
    other_multi_family_use_codes = [
        string
        for string in [str(num) for num in range(106, 154 + 1)]
        if string not in ["104", "105", "109", "111", "112", "113", "114", "115"]
    ]

    parcel_data["isUsedAsSF"] = parcel_data["USE_CODE"].apply(
        lambda use_code: use_code in single_family_usage_codes
    )
    parcel_data["isUsedAsCommercial"] = parcel_data["USE_CODE"].apply(
        lambda use_code: use_code in commercial_use_codes
    )
    parcel_data["isUsedAsDuplex"] = parcel_data["USE_CODE"].apply(
        lambda use_code: use_code in duplex_use_codes
    )
    parcel_data["isUsedAsTriplex"] = parcel_data["USE_CODE"].apply(
        lambda use_code: use_code in triplex_use_codes
    )
    parcel_data["isUsedAsMultiBuildings1Lot"] = parcel_data["USE_CODE"].apply(
        lambda use_code: use_code in multi_buildings_1lot_use_codes
    )
    parcel_data["isUsedAsAptUpTo30Units"] = parcel_data["USE_CODE"].apply(
        lambda use_code: use_code in apt_up_to_30_units_use_codes
    )
    parcel_data["isUsedAsAptOver30Units"] = parcel_data["USE_CODE"].apply(
        lambda use_code: use_code in apt_over_30_units_use_codes
    )
    parcel_data["isUsedAsCoopApt"] = parcel_data["USE_CODE"].apply(
        lambda use_code: use_code in coop_apt_use_codes
    )
    parcel_data["isUsedAsOtherMultifamily"] = parcel_data["USE_CODE"].apply(
        lambda use_code: use_code in other_multi_family_use_codes
    )

    parcel_data["mustUpzone"] = parcel_data.apply(
        lambda row: True if row["isZonedAsSF"] else False, axis=1
    )
    parcel_data["willChange"] = parcel_data.apply(
        lambda row: True if (row["isZonedAsSF"] and row["isUsedAsSF"]) else False,
        axis=1,
    )

    return parcel_data


def percentage_true(series):
    return (series.sum() / len(series)) * 100


def aggregate_zoning_usage_by_stop_zone(parcel_data: gpd.GeoDataFrame) -> pd.DataFrame:

    # parcel geography is eliminated in the agg, returns a dataframe

    stop_zone_data = (
        parcel_data.groupby("stop_name")
        .agg(
            {
                "municipality": "first",
                "isZonedAsSF": percentage_true,
                "isZonedAsCommercial": percentage_true,
                "isZonedAsMultifamily": percentage_true,
                "isUsedAsSF": percentage_true,
                "isUsedAsCommercial": percentage_true,
                "isUsedAsDuplex": percentage_true,
                "isUsedAsTriplex": percentage_true,
                "isUsedAsMultiBuildings1Lot": percentage_true,
                "isUsedAsAptUpTo30Units": percentage_true,
                "isUsedAsAptOver30Units": percentage_true,
                "isUsedAsCoopApt": percentage_true,
                "isUsedAsOtherMultifamily": percentage_true,
                "mustUpzone": percentage_true,
                "willChange": percentage_true,
            }
        )
        .reset_index()
    )

    stop_zone_data.rename(
        columns={
            "isZonedAsSF": "pctZonedAsSF",
            "isZonedAsCommercial": "pctZonedAsCommercial",
            "isZonedAsMultifamily": "pctZonedAsMultifamily",
            "isUsedAsSF": "pctUsedAsSF",
            "isUsedAsCommercial": "pctUsedAsCommercial",
            "isUsedAsDuplex": "pctUsedAsDuplex",
            "isUsedAsTriplex": "pctUsedAsTriplex",
            "isUsedAsMultiBuildings1Lot": "pctUsedAsMultiBuildings1Lot",
            "isUsedAsAptUpTo30Units": "pctUsedAsAptUpTo30Units",
            "isUsedAsAptOver30Units": "pctUsedAsAptOver30Units",
            "isUsedAsCoopApt": "pctUsedAsCoopApt",
            "isUsedAsOtherMultifamily": "pctUsedAsOtherMultifamily",
            "mustUpzone": "pctMustUpzone",
            "willChange": "pctWillChange",
        },
        inplace=True,
    )

    # TODO: subtract actual categories from zoning so that it's not 100
    stop_zone_data["pctOtherZoning"] = 100 - (
        stop_zone_data["pctZonedAsSF"]
        + stop_zone_data["pctZonedAsCommercial"]
        + stop_zone_data["pctZonedAsMultifamily"]
    )
    stop_zone_data["pctOtherUsage"] = 100 - (
        stop_zone_data["pctUsedAsSF"]
        + stop_zone_data["pctUsedAsCommercial"]
        + stop_zone_data["pctUsedAsDuplex"]
        + stop_zone_data["pctUsedAsTriplex"]
        + stop_zone_data["pctUsedAsMultiBuildings1Lot"]
        + stop_zone_data["pctUsedAsAptUpTo30Units"]
        + stop_zone_data["pctUsedAsAptOver30Units"]
        + stop_zone_data["pctUsedAsCoopApt"]
        + stop_zone_data["pctUsedAsOtherMultifamily"]
    )

    return stop_zone_data


def augment_parcels_for_upzone_viz(parcel_data_zoning_usage: gpd.GeoDataFrame):

    selected_cols = parcel_data_zoning_usage[
        ["municipality", "stop_name", "geometry", "mustUpzone", "willChange"]
    ]

    return selected_cols


if __name__ == "__main__":
    start = time.time()
    municipalities_count = 0
    stops_count = 0
    zoning_atlas = pd.read_csv(DATA_PATH / "zoning_atlas.csv")

    file_name_reference = pd.read_csv(
        f"{STATIC_SITE_DATA_PATH}/parcels/raw_parcels_file_name_reference.csv"
    )

    census_data_by_stop_zone = gpd.read_file(
        STATIC_SITE_DATA_PATH / "mbta_community_stops_with_buffer_and_census.geojson"
    )

    rows = []

    # filenames = [f'data/parcels/per_station/{file}' for file in os.listdir(f"{DATA_PATH}/raw_parcels")]

    # print([
    #     file for file in filenames
    #     if file not in
    #     file_name_reference["FileName"].unique()
    # ])

    # TODO: figure out why R2 is not contained in the single family. in general need to inspect the single family zoning

    for filename in os.listdir(f"{DATA_PATH}/raw_parcels"):
        # [f"{DATA_PATH}/parcels/alewife_parcels.geojson"]:

        # os.listdir(f"{DATA_PATH}/raw_parcels"):

        try:
            station = file_name_reference[
                file_name_reference["FileName"]
                == f"data/parcels/per_station/{filename}"
            ]["StopName"].values[0]

        except IndexError:
            print(f"Reference for {filename} not found ")
            print(file_name_reference["FileName"].unique())

            continue

        station_formatted = station.lower().replace(" ", "_").replace("/", "_")

        try:
            # read in raw parcel data for station
            actual_filename = f"{DATA_PATH}/raw_parcels/{filename}"
            parcels_for_station = gpd.read_file(actual_filename)
            print(f"SUCCESS for {actual_filename}")

        except FionaValueError:
            print(f"File for {actual_filename} not found.")
            continue

        # get the city associated with the station so can look up zoning codes.
        municipality = parcels_for_station["TOWN_NAME"].unique()[0]

        zoning_atlas_for_municipality = zoning_atlas[
            zoning_atlas["muni"] == municipality
        ]

        if len(zoning_atlas_for_municipality) == 0:
            print(f"Zoning atlas information for {municipality} not found.")
            continue

        # assign zoning and usage to the parcel based on codes
        parcels_for_station_zoning = assign_zoning_by_parcel(
            zoning_atlas_for_municipality, parcels_for_station
        )
        parcel_data_zoning_usage = assign_usage_by_parcel(parcels_for_station_zoning)

        augemented_parcels_for_station = augment_parcels_for_upzone_viz(
            parcel_data_zoning_usage
        )

        try:
            # write out augmented parcels by station
            augemented_parcels_for_station.to_file(
                STATIC_SITE_DATA_PATH
                / f"parcels/per_station/{station_formatted}_augmented_parcels.geojson",
                driver="GeoJSON",
            )
            print(f"Wrote out augmented parcels for {station_formatted}")

        except FionaValueError:
            print(f"File for {actual_filename} not found.")
            continue

        selected_stop_zones_usage_zoning = aggregate_zoning_usage_by_stop_zone(
            parcel_data_zoning_usage
        )

        assert isinstance(
            census_data_by_stop_zone, gpd.GeoDataFrame
        ), "census_data_by_stop_zone is not a GeoDataFrame"

        stop_zone_zoning_usage_census = pd.merge(
            census_data_by_stop_zone, selected_stop_zones_usage_zoning
        )

        # rows.append({
        #     'StopName':
        #     station,
        #     'FileName':
        #     f"data/stop_zones/per_station/{station_formatted}_stop_zone.geojson"
        # })

        # stop_zone_zoning_usage_census.to_file(
        #     STATIC_SITE_DATA_PATH /
        #     f"stop_zones/per_station/{station_formatted}_stop_zone.geojson",
        #     driver='GeoJSON')

        municipalities_count += 1
        stops_count += len(stop_zone_zoning_usage_census)
    end = time.time()
    file_name_reference = pd.DataFrame(rows, columns=["StopName", "FileName"])
    file_name_reference.to_csv(
        STATIC_SITE_DATA_PATH / "stop_zones/file_name_reference.csv", index=False
    )
    print(
        "Time elapsed:",
        end - start,
        f"to transform data from {municipalities_count} municipalities totaling {stops_count} stops",
    )
