import geopandas as gpd
from pathlib import Path
import pandas as pd
import time
import data_generation_helpers as helpers
from fiona.errors import FionaValueError
import os

PREPROCESSED_DATA_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/6.C85_FP/data/preprocessed_data"
)

DATA_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/6.C85_FP/data"
)

STATIC_SITE_DATA_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/6.C85_FP/code/static/data"
)


def assign_zoning_by_parcel(
        zoning_atlas_for_municipality: str,
        parcel_data_for_municipality: pd.DataFrame) -> pd.DataFrame:

    sf_zoning_codes = helpers.get_zoning_codes_for_type_for_municipality(
        zoning_atlas_for_municipality, ["Single"])
    multifamily_zoning_codes = helpers.get_zoning_codes_for_type_for_municipality(
        zoning_atlas_for_municipality, ['Multi Family', 'Multiple Family'])
    commercial_zoning_codes = helpers.get_zoning_codes_for_type_for_municipality(
        zoning_atlas_for_municipality, ["Commercial"])

    sf_zoning_codes = list(
        set(sf_zoning_codes) - set(multifamily_zoning_codes)
    )  # the single family codes that do not include multifamily. some codes encompass multi and single and these should be considered multifamily for this analysis

    commercial_zoning_codes = list(
        set(commercial_zoning_codes) - set(multifamily_zoning_codes)
    )  # similarly, decide that areas that are both multifamily and commercial are just multifamily

    parcel_data_for_municipality['isZonedAsSF'] = parcel_data_for_municipality[
        'ZONING'].apply(lambda zoning_code: zoning_code in sf_zoning_codes)
    parcel_data_for_municipality[
        'isZonedAsMultifamily'] = parcel_data_for_municipality['ZONING'].apply(
            lambda zoning_code: zoning_code in multifamily_zoning_codes)
    parcel_data_for_municipality[
        'isZonedAsCommercial'] = parcel_data_for_municipality['ZONING'].apply(
            lambda zoning_code: zoning_code in commercial_zoning_codes)

    return parcel_data_for_municipality


def assign_usage_by_parcel(parcel_data: pd.DataFrame) -> pd.DataFrame:

    # Assign usage by parcel
    # these are for all of Massachusetts: https://www.cityofboston.gov/images_documents/ma_occcodes_tcm3-16189.pdf
    single_family_usage_codes = ['101']
    commercial_use_codes = [str(num)
                            for num in range(310, 399 + 1)]  # remove parking?
    duplex_use_codes = ['104']
    triplex_use_codes = ['105']
    multi_buildings_1lot_use_codes = ['109']
    apt_up_to_30_units_use_codes = ['111', '112']
    apt_over_30_units_use_codes = ['113', '114']
    coop_apt_use_codes = ['115']
    other_multi_family_use_codes = [
        string for string in [str(num) for num in range(106, 154 + 1)] if
        string not in ['104', '105', '109', '111', '112', '113', '114', '115']
    ]

    parcel_data['isUsedAsSF'] = parcel_data['USE_CODE'].apply(
        lambda use_code: use_code in single_family_usage_codes)
    parcel_data['isUsedAsCommercial'] = parcel_data['USE_CODE'].apply(
        lambda use_code: use_code in commercial_use_codes)
    parcel_data['isUsedAsDuplex'] = parcel_data['USE_CODE'].apply(
        lambda use_code: use_code in duplex_use_codes)
    parcel_data['isUsedAsTriplex'] = parcel_data['USE_CODE'].apply(
        lambda use_code: use_code in triplex_use_codes)
    parcel_data['isUsedAsMultiBuildings1Lot'] = parcel_data['USE_CODE'].apply(
        lambda use_code: use_code in multi_buildings_1lot_use_codes)
    parcel_data['isUsedAsAptUpTo30Units'] = parcel_data['USE_CODE'].apply(
        lambda use_code: use_code in apt_up_to_30_units_use_codes)
    parcel_data['isUsedAsAptOver30Units'] = parcel_data['USE_CODE'].apply(
        lambda use_code: use_code in apt_over_30_units_use_codes)
    parcel_data['isUsedAsCoopApt'] = parcel_data['USE_CODE'].apply(
        lambda use_code: use_code in coop_apt_use_codes)
    parcel_data['isUsedAsOtherMultifamily'] = parcel_data['USE_CODE'].apply(
        lambda use_code: use_code in other_multi_family_use_codes)

    parcel_data['mustUpzone'] = parcel_data.apply(
        lambda row: True if row['isZonedAsSF'] else False, axis=1)
    parcel_data['willChange'] = parcel_data.apply(
        lambda row: True
        if (row['isZonedAsSF'] and row['isUsedAsSF']) else False,
        axis=1)

    return parcel_data


def percentage_true(series):
    return (series.sum() / len(series)) * 100


def aggregate_zoning_usage_by_stop_zone(
        parcel_data: gpd.GeoDataFrame) -> pd.DataFrame:

    # parcel geography is eliminated in the agg, returns a dataframe

    stop_zone_data = parcel_data.groupby('stop_name').agg({
        'municipality':
        'first',
        'isZonedAsSF':
        percentage_true,
        'isZonedAsCommercial':
        percentage_true,
        'isZonedAsMultifamily':
        percentage_true,
        'isUsedAsSF':
        percentage_true,
        'isUsedAsCommercial':
        percentage_true,
        'isUsedAsDuplex':
        percentage_true,
        'isUsedAsTriplex':
        percentage_true,
        'isUsedAsMultiBuildings1Lot':
        percentage_true,
        'isUsedAsAptUpTo30Units':
        percentage_true,
        'isUsedAsAptOver30Units':
        percentage_true,
        'isUsedAsCoopApt':
        percentage_true,
        'isUsedAsOtherMultifamily':
        percentage_true,
        'mustUpzone':
        percentage_true,
        'willChange':
        percentage_true,
    }).reset_index()

    stop_zone_data.rename(columns={
        'isZonedAsSF': 'pctZonedAsSF',
        'isZonedAsCommercial': 'pctZonedAsCommercial',
        'isZonedAsMultifamily': 'pctZonedAsMultifamily',
        'isUsedAsSF': 'pctUsedAsSF',
        'isUsedAsCommercial': 'pctUsedAsCommercial',
        'isUsedAsDuplex': 'pctUsedAsDuplex',
        'isUsedAsTriplex': 'pctUsedAsTriplex',
        'isUsedAsMultiBuildings1Lot': 'pctUsedAsMultiBuildings1Lot',
        'isUsedAsAptUpTo30Units': 'pctUsedAsAptUpTo30Units',
        'isUsedAsAptOver30Units': 'pctUsedAsAptOver30Units',
        'isUsedAsCoopApt': 'pctUsedAsCoopApt',
        'isUsedAsOtherMultifamily': 'pctUsedAsOtherMultifamily',
        'mustUpzone': 'pctMustUpzone',
        'willChange': 'pctWillChange'
    },
                          inplace=True)

    stop_zone_data['pctOtherZoning'] = 100 - (
        stop_zone_data['pctZonedAsSF'] + stop_zone_data['pctZonedAsCommercial']
        + stop_zone_data['pctZonedAsMultifamily'])
    stop_zone_data['pctOtherUsage'] = 100 - (
        stop_zone_data['pctUsedAsSF'] + stop_zone_data['pctUsedAsCommercial'] +
        stop_zone_data['pctUsedAsDuplex'] + stop_zone_data['pctUsedAsTriplex']
        + stop_zone_data['pctUsedAsMultiBuildings1Lot'] +
        stop_zone_data['pctUsedAsAptUpTo30Units'] +
        stop_zone_data['pctUsedAsAptOver30Units'] +
        stop_zone_data['pctUsedAsCoopApt'] +
        stop_zone_data['pctUsedAsOtherMultifamily'])

    return stop_zone_data


def augment_parcels_for_upzone_viz(parcel_data_zoning_usage: gpd.GeoDataFrame):

    selected_cols = parcel_data_zoning_usage[[
        "municipality", "stop_name", "geometry", "mustUpzone", "willChange"
    ]]

    return selected_cols


if __name__ == "__main__":
    start = time.time()
    municipalities_count = 0
    stops_count = 0
    zoning_atlas = pd.read_csv(DATA_PATH / 'zoning_atlas.csv')

    file_name_reference = pd.read_csv(
        f"{STATIC_SITE_DATA_PATH}/file_name_reference.csv")

    for filename in os.listdir(f"{STATIC_SITE_DATA_PATH}/parcels/per_station"):

        station = file_name_reference[file_name_reference["FileName"] ==
                                      filename]["StopName"]

        try:
            actual_filename = f"{STATIC_SITE_DATA_PATH}/parcels/per_station/{filename}"
            selected_parcels = gpd.read_file(actual_filename)
            print(f"SUCCESS for {actual_filename}")

        except FionaValueError:
            print(f"File for {actual_filename} not found.")
            continue

        municipality = selected_parcels["TOWN_NAME"].unique()[0]
        zoning_atlas_for_municipality = zoning_atlas[zoning_atlas["muni"] ==
                                                     municipality]

        if len(zoning_atlas_for_municipality) == 0:
            print(f"Zoning atlas information for {municipality} not found.")
            continue
        selected_parcels_zoning = assign_zoning_by_parcel(
            zoning_atlas_for_municipality, selected_parcels)
        parcel_data_zoning_usage = assign_usage_by_parcel(
            selected_parcels_zoning)

        augemented_parcels = augment_parcels_for_upzone_viz(
            parcel_data_zoning_usage)

        augemented_parcels.to_file(
            STATIC_SITE_DATA_PATH /
            f"parcels/will_change/{municipality.lower()}_parcels_for_upzone_willchange_viz.geojson",
            driver='GeoJSON')

        selected_stop_zones_usage_zoning = aggregate_zoning_usage_by_stop_zone(
            parcel_data_zoning_usage)

        census_data_by_stop_zone = gpd.read_file(
            STATIC_SITE_DATA_PATH /
            'mbta_community_stops_with_buffer_and_census.geojson')

        assert isinstance(
            census_data_by_stop_zone,
            gpd.GeoDataFrame), "census_data_by_stop_zone is not a GeoDataFrame"

        stop_zone_zoning_usage_census = pd.merge(
            census_data_by_stop_zone, selected_stop_zones_usage_zoning)

        stop_zone_zoning_usage_census.to_file(
            STATIC_SITE_DATA_PATH /
            f"stop_zones/{municipality.lower()}_stop_zone_census.geojson",
            driver='GeoJSON')
        municipalities_count += 1
        stops_count += len(stop_zone_zoning_usage_census)
    end = time.time()
    print(
        'Time elapsed:', end - start,
        f'to transform data from {municipalities_count} municipalities totaling {stops_count} stops'
    )
