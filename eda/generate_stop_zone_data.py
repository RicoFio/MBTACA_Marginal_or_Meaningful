import geopandas as gpd
from pathlib import Path
import pandas as pd
import json

PREPROCESSED_DATA_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/6.C85_FP/data/preprocessed_data"
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


def aggregate_statistics_by_stop_zone(
        parcel_data: pd.DataFrame) -> pd.DataFrame:

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
        'isZonedAsCommmercial': 'pctZonedAsCommercial',
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

    stop_zone_data['pctFutureZonedAsSF'] = stop_zone_data[
        'pctZonedAsSF'] - stop_zone_data['pctMustUpzone']
    stop_zone_data['pctFutureZonedAsMulti'] = stop_zone_data[
        'pctZonedAsMultifamily'] + stop_zone_data['pctMustUpzone']

    return stop_zone_data


def combine_census_data_to_stop_name_level(
        census_data: pd.DataFrame) -> pd.DataFrame:

    rename_dict = {
        'stop_name':
        'stop_name',
        'weighted_Total Population':
        'weighted_total_population',
        'weighted_Population Density (Per Sq. Mile)':
        'weighted_total_population_density_permile',
        'weighted_Total Population: Male':
        'weighted_total_population_male',
        'weighted_Total Population: Female':
        'weighted_total_population_female',
        'weighted_% Total Population: Male':
        'weighted_pct_population_male',
        'weighted_% Total Population: Female':
        'weighted_pct_population_female',
        'weighted_% Total Population: Not Hispanic or Latino':
        'weighted_pct_not_hispanic_latino',
        'weighted_% Total Population: Not Hispanic or Latino: White Alone':
        'weighted_pct_not_hispanic_latino_white',
        'weighted_% Total Population: Not Hispanic or Latino: Black or African American Alone':
        'weighted_pct_not_hispanic_latino_black',
        'weighted_% Total Population: Not Hispanic or Latino: American Indian and Alaska Native Alone':
        'weighted_pct_not_hispanic_latino_native',
        'weighted_% Total Population: Not Hispanic or Latino: Asian Alone':
        'weighted_pct_not_hispanic_latino_asian',
        'weighted_% Total Population: Not Hispanic or Latino: Native Hawaiian and Other Pacific Islander Alone':
        'weighted_pct_not_hispanic_latino_pi',
        'weighted_% Total Population: Not Hispanic or Latino: Some Other Race Alone':
        'weighted_pct_not_hispanic_latino_other',
        'weighted_% Total Population: Not Hispanic or Latino: Two or More Races':
        'weighted_pct_not_hispanic_latino_2+',
        'weighted_% Total Population: Hispanic or Latino':
        'weighted_pct_hispanic_latino',
        'weighted_% Total Population: Hispanic or Latino: White Alone':
        'weighted_pct_hispanic_latino_white',
        'weighted_% Total Population: Hispanic or Latino: Black or African American Alone':
        'weighted_pct_hispanic_latino_black',
        'weighted_% Total Population: Hispanic or Latino: American Indian and Alaska Native Alone':
        'weighted_pct_hispanic_latino_native',
        'weighted_% Total Population: Hispanic or Latino: Asian Alone':
        'weighted_pct_hispanic_latino_asian',
        'weighted_% Total Population: Hispanic or Latino: Native Hawaiian and Other Pacific Islander Alone':
        'weighted_pct_hispanic_latino_pi',
        'weighted_% Total Population: Hispanic or Latino: Some Other Race Alone':
        'weighted_pct_hispanic_latino_other',
        'weighted_% Total Population: Hispanic or Latino: Two or More Races':
        'weighted_pct_hispanic_latino_2+',
        'weighted_Median Household Income (In 2022 Inflation Adjusted Dollars)':
        'weighted_median_hh_income',
        'weighted_% Workers 16 Years and Over: Car, Truck, or Van':
        'pct_workers_car_van',
        'weighted_% Workers 16 Years and Over: Drove Alone':
        'pct_workers_drive_alone',
        'weighted_% Workers 16 Years and Over: Carpooled':
        'pct_workers_drive_carpooled',
        'weighted_% Workers 16 Years and Over: Public Transportation (Includes Taxicab)':
        'pct_workers_public_transportation',
        'weighted_% Workers 16 Years and Over: Motorcycle':
        'pct_workers_motorcycle',
        'weighted_% Workers 16 Years and Over: Bicycle':
        'pct_workers_bicycle',
        'weighted_% Workers 16 Years and Over: Walked':
        'pct_workers_walked',
        'weighted_% Workers 16 Years and Over: Other Means':
        'pct_workers_other',
        'weighted_% Workers 16 Years and Over: Worked At Home':
        'pct_workers_wfh',
        'weighted_% Occupied Housing Units: No Vehicle Available':
        'pct_hh_0_vehs',
        'weighted_% Occupied Housing Units: 1 Vehicle Available':
        'pct_hh_1_vehs',
        'weighted_% Occupied Housing Units: 2 Vehicles Available':
        'pct_hh_2_vehs',
        'weighted_% Occupied Housing Units: 3 Vehicles Available':
        'pct_hh_3_vehs',
        'weighted_% Occupied Housing Units: 4 Vehicles Available':
        'pct_hh_4_vehs',
        'weighted_% Occupied Housing Units: 5 or More Vehicles Available':
        'pct_hh_5_vehs',
        'geometry':
        'geometry'
    }

    dataframe_columns = set(census_data.columns)
    dictionary_keys = set(rename_dict.keys())
    assert dictionary_keys.issubset(dataframe_columns)

    census_data.rename(columns=rename_dict, inplace=True)

    census_data = census_data[list(rename_dict.values())]

    census_data_agg_by_stop_name = census_data.groupby('stop_name').agg({
        col:
        'mean' if census_data[col].dtype == 'float64'
        or census_data[col].dtype == 'int64' else 'first'
        for col in census_data.columns
    })

    census_data_agg_by_stop_name.drop('stop_name', axis=1, inplace=True)

    census_data_agg_by_stop_name = census_data_agg_by_stop_name.reset_index()

    census_data_agg_by_stop_name_gdf = gpd.GeoDataFrame(
        census_data_agg_by_stop_name)

    return census_data_agg_by_stop_name_gdf


def generate_stop_zones_with_zoning_usage_census(parcel_data):

    parcels_zoning = assign_zoning_by_parcel(parcel_data)
    parcel_data_zoning_usage = assign_usage_by_parcel(parcels_zoning)

    station_buffer_census_cumulative = gpd.read_file(
        PREPROCESSED_DATA_PATH / 'station_buffer_census_cumulative.geojson')
    modified_census_data = combine_census_data_to_stop_name_level(
        station_buffer_census_cumulative)
    print("num unique stop names census data",
          len(modified_census_data["stop_name"].unique()))

    stop_zone_data_zoning_usage = aggregate_statistics_by_stop_zone(
        parcel_data_zoning_usage)
    print("num unique stop names stop zone  data",
          len(stop_zone_data_zoning_usage["stop_name"].unique()))

    stop_zone_census = modified_census_data.merge(stop_zone_data_zoning_usage,
                                                  on="stop_name")

    #TODO: need to better reconcile the stop names.
    stop_zone_census_without_duplicate_stops = stop_zone_census.drop_duplicates(
        subset=['stop_name'], keep='first')

    return stop_zone_census_without_duplicate_stops


if __name__ == "__main__":
    brookline_milton_parcels = gpd.read_file(
        PREPROCESSED_DATA_PATH / 'brookline_milton_parcels.geojson')
    stop_zone_census = generate_stop_zones_with_zoning_usage_census(
        brookline_milton_parcels)

    stop_zone_census.to_file(PREPROCESSED_DATA_PATH /
                             "brookline_milton_stop_zone_census.geojson",
                             driver='GeoJSON')
