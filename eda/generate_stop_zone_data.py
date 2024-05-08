import geopandas as gpd
from pathlib import Path
import pandas as pd
import json
import time

PREPROCESSED_DATA_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/6.C85_FP/data/preprocessed_data"
)

STATIC_SITE_DATA_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/6.C85_FP/code/static/data"
)


def get_parcel_data_filtered_by_municipalities(municipalities):

    parcels_within_station_buffer = gpd.read_file(
        PREPROCESSED_DATA_PATH / 'station_only_parcels.geojson')
    brookline_milton_parcels = parcels_within_station_buffer[
        parcels_within_station_buffer["municipality"].isin(municipalities)]
    brookline_milton_parcels['zone_id'] = brookline_milton_parcels[
        'zone_id'].apply(json.dumps)
    brookline_milton_parcels['routes'] = brookline_milton_parcels[
        'routes'].apply(json.dumps)
    brookline_milton_parcels['route_colors'] = brookline_milton_parcels[
        'route_colors'].apply(json.dumps)
    # write the brookline and milton parcels to a file so don't have to keep reading the big file in
    # brookline_milton_parcels.to_file(PREPROCESSED_DATA_PATH /
    #                                 "brookline_milton_parcels.geojson",
    #                                 driver='GeoJSON')


def assign_zoning_by_parcel(parcel_data: pd.DataFrame) -> pd.DataFrame:

    # these are for brookline, will need to see if they scale https://www.brooklinema.gov/DocumentCenter/View/19956/GIS---Zoning-Map-10CC-11x17pdf
    #TODO: use some kind of fuzzy matching for these
    sf_zoning_codes = [
        'S-40', 'S-25', 'S-15', 'S-10', 'S-7', 'S-4', 'S-0.5P,'
        'S-0.75P', 'SC-7', 'SC-10', 'T-6', 'T-5', 'SF', 'S10', 'S40', 'S25',
        'S15', 'S7', 'S4', 'R1'
    ]
    multifamily_zoning_codes = [
        'F10', 'M-0.5', 'M5', 'M10', 'M10(CAM)', 'M15', 'M20', 'M25'
    ]  #the zoning code says M1.0, M1.5, but the data has it has M10, M15, etc.
    commercial_zoning_codes = [
        'L-0.5', 'L-0.5(CL)', 'L-1.0', 'G-1.0', 'G-(DP)', 'G-1.75(CC)',
        'G-1.75(LSH)', 'G-1.75(WS)', 'G-2.0', 'G-2.0(CA)', 'GMR-2.0', 'O-1.0',
        'O-2.0(CH)', 'G175(LSH', 'G10', 'G20', 'G175(WS)', 'G175(CC)', 'G(DP)',
        'G', 'GU', 'GR', 'GB', 'GI', 'G RS', 'GC', 'GBD', 'GD', 'G20',
        'G175(CC)', 'G175(WS)', 'G175(LSH', 'G10', 'GMR20', 'G(DP)', 'GRA',
        'GRB'
    ]

    parcel_data['isZonedAsSF'] = parcel_data['ZONING'].apply(
        lambda zoning_code: zoning_code in sf_zoning_codes)
    parcel_data['isZonedAsMultifamily'] = parcel_data['ZONING'].apply(
        lambda zoning_code: zoning_code in multifamily_zoning_codes)
    parcel_data['isZonedAsCommercial'] = parcel_data['ZONING'].apply(
        lambda zoning_code: zoning_code in commercial_zoning_codes)

    return parcel_data


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


def generate_stop_zones_with_zoning_usage(parcel_data):

    parcels_zoning = assign_zoning_by_parcel(parcel_data)
    parcel_data_zoning_usage = assign_usage_by_parcel(parcels_zoning)

    selected_stop_zones_usage_zoning = aggregate_zoning_usage_by_stop_zone(
        parcel_data_zoning_usage)

    return selected_stop_zones_usage_zoning


if __name__ == "__main__":
    start = time.time()
    selected_communities = ["Brookline", "Milton"]
    file_name = '_'.join(selected_communities).lower()
    selected_parcels = gpd.read_file(PREPROCESSED_DATA_PATH /
                                     f'{file_name}_parcels.geojson')

    selected_stop_zones_usage_zoning = generate_stop_zones_with_zoning_usage(
        selected_parcels)

    census_data_by_stop_zone = gpd.read_file(
        STATIC_SITE_DATA_PATH /
        'mbta_community_stops_with_buffer_and_census.geojson')

    assert isinstance(
        census_data_by_stop_zone,
        gpd.GeoDataFrame), "census_data_by_stop_zone is not a GeoDataFrame"

    stop_zone_zoning_usage_census = pd.merge(census_data_by_stop_zone,
                                             selected_stop_zones_usage_zoning)

    stop_zone_zoning_usage_census.to_file(
        STATIC_SITE_DATA_PATH / f"{file_name}_stop_zone_census.geojson",
        driver='GeoJSON')
    end = time.time()
    print('Time elapsed:', end-start, f'to transform {len(selected_parcels)} parcels from {len(selected_communities)}')
