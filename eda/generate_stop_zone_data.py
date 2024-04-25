import geopandas as gpd
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json

PREPROCESSED_DATA_PATH = Path(
    "/Users/ameliabaum/Library/Mobile Documents/com~apple~CloudDocs/MIT/6.C35/6.C85_FP/data/preprocessed_data"
)

# parcels_within_station_buffer = gpd.read_file(PREPROCESSED_DATA_PATH /
#                                               'station_only_parcels.geojson')
# brookline_milton_parcels = parcels_within_station_buffer[
#     (parcels_within_station_buffer["municipality"] == 'Brookline') |
#     (parcels_within_station_buffer["municipality"] == "Milton")]
# brookline_milton_parcels['zone_id'] = brookline_milton_parcels[
#     'zone_id'].apply(json.dumps)
# brookline_milton_parcels['routes'] = brookline_milton_parcels['routes'].apply(
#     json.dumps)
# brookline_milton_parcels['route_colors'] = brookline_milton_parcels[
#     'route_colors'].apply(json.dumps)
# # write the brookline and milton parcels to a file so don't have to keep reading the big file in
# brookline_milton_parcels.to_file(PREPROCESSED_DATA_PATH /
#                                  "brookline_milton_parcels.geojson",
#                                  driver='GeoJSON')

brookline_milton_parcels = gpd.read_file(PREPROCESSED_DATA_PATH /
                                              'brookline_milton_parcels.geojson')
print(len(brookline_milton_parcels))

# Assign zoning by parcel

# these are for brookline, will need to see if they scale https://www.brooklinema.gov/DocumentCenter/View/19956/GIS---Zoning-Map-10CC-11x17pdf
sf_zoning_codes = ['S-40', 'S-25', 'S-15', 'S-10', 'S-7', 'S-4', 'S-0.5P,' 'S-0.75P', 'SC-7', 'SC-10', 'T-6', 'T-5', 'SF', 'S10', 'S40', 'S25', 'S15', 'S7', 'S4']
multifamily_zoning_codes = ['F10', 'M-0.5', 'M5', 'M10', 'M10(CAM)', 'M15', 'M20', 'M25'] #the zoning code says M1.0, M1.5, but the data has it has M10, M15, etc.
commercial_zoning_codes = [
    'L-0.5', 'L-0.5(CL)', 'L-1.0', 'G-1.0', 'G-(DP)', 'G-1.75(CC)',
    'G-1.75(LSH)', 'G-1.75(WS)', 'G-2.0', 'G-2.0(CA)', 'GMR-2.0', 'O-1.0',
    'O-2.0(CH)', 'G175(LSH', 'G10', 'G20', 'G175(WS)', 'G175(CC)', 'G(DP)',
    'G', 'GU', 'GR', 'GB', 'GI', 'G RS', 'GC', 'GBD', 'GD', 'G20', 'G175(CC)',
    'G175(WS)', 'G175(LSH', 'G10', 'GMR20', 'G(DP)', 'GRA', 'GRB'
]

brookline_milton_parcels['isSFZoning'] = brookline_milton_parcels[
    'ZONING'].apply(lambda zoning_code: zoning_code in sf_zoning_codes)
brookline_milton_parcels['isMultiFamZoning'] = brookline_milton_parcels[
    'ZONING'].apply(
        lambda zoning_code: zoning_code in multifamily_zoning_codes)
brookline_milton_parcels['isCommercialZoning'] = brookline_milton_parcels[
    'ZONING'].apply(lambda zoning_code: zoning_code in commercial_zoning_codes)

# Assign usage by parcel
# these are for all of Massachusetts: https://www.cityofboston.gov/images_documents/ma_occcodes_tcm3-16189.pdf
single_family_usage_codes = ['101']
commercial_use_codes = [str(num) for num in range(310, 399 + 1)] # remove parking?
duplex_use_codes = ['104']
triplex_use_codes = ['105']
multi_buildings_1lot_use_codes = ['109']
apt_up_to_30_units_use_codes = ['111', '112']
apt_over_30_units_use_codes = ['113', '114']
coop_apt_use_codes = ['115']
other_multi_family_use_codes = [string for string in [str(num) for num in range(106, 154 + 1)] if string not in ['104', '105', '109', '111', '112', '113', '114', '115']]


brookline_milton_parcels['isUsedAsSF'] = brookline_milton_parcels[
    'USE_CODE'].apply(lambda use_code: use_code in single_family_usage_codes)
brookline_milton_parcels['isUsedAsComm'] = brookline_milton_parcels[
    'USE_CODE'].apply(lambda use_code: use_code in commercial_use_codes)
brookline_milton_parcels['isUsedAsDuplex'] = brookline_milton_parcels[
    'USE_CODE'].apply(lambda use_code: use_code in duplex_use_codes)
brookline_milton_parcels['isUsedAsTriplex'] = brookline_milton_parcels[
    'USE_CODE'].apply(lambda use_code: use_code in triplex_use_codes)
brookline_milton_parcels['isUsedAsMultiBuildings1Lot'] = brookline_milton_parcels[
    'USE_CODE'].apply(lambda use_code: use_code in multi_buildings_1lot_use_codes)
brookline_milton_parcels['isUsedAsAptUpTo30Units'] = brookline_milton_parcels[
    'USE_CODE'].apply(lambda use_code: use_code in apt_up_to_30_units_use_codes)
brookline_milton_parcels['isUsedAsAptOver30Units'] = brookline_milton_parcels[
    'USE_CODE'].apply(lambda use_code: use_code in apt_over_30_units_use_codes)
brookline_milton_parcels['isUsedAsCoopApt'] = brookline_milton_parcels[
    'USE_CODE'].apply(lambda use_code: use_code in coop_apt_use_codes)
brookline_milton_parcels['isUsedAsOtherMultifamily'] = brookline_milton_parcels[
    'USE_CODE'].apply(lambda use_code: use_code in other_multi_family_use_codes)


brookline_milton_parcels['mustUpzone'] = brookline_milton_parcels.apply(lambda row: True if row['isZonedAsSF'] else False, axis=1)
brookline_milton_parcels['willChange'] = brookline_milton_parcels.apply(
    lambda row: True if (row['isZonedAsSF'] and row['isUsedAsSF']) else False,
    axis=1)

# group parcels into stop zones by stop_name

# add in census data


# add in stop zone geographies