import os.path
from datetime import datetime

import pandas as pd
import netCDF4
from azure.storage.blob import BlobServiceClient

from munpy import config
from munpy.general import get_nc_index, db_to_street_center
from munpy.io import dumpBinary
from munpy.preprocessing.meteo_functions import *


STREET_PARAMETERS = [
    'WindDirection', 'WindSpeed', 'PBLH', 'UST', 'LMO',
    'SpecificHumidity', 'SurfaceTemperature', 'LiquidWaterContent',
    'SolarRadiation', 'Rain', 'SurfacePressure'
]

INTER_PARAMETERS = [
    'WindDirection', 'WindSpeed',
    'PBLH', 'LMO', 'UST'
]


def get_param(parameter, latitude, longitude, ncdataset):
    """

    :param parameter: parameter to obtain
    :param latitude:
    :param longitude:
    :param ncdataset: WRF dataset
    :return:
    """

    i_index, j_index, _ = get_nc_index(latitude, longitude, ncdataset)

    if parameter == 'WindDirection':
        u_wind = ncdataset.variables[config.U_WIND][:, i_index, j_index]
        v_wind = ncdataset.variables[config.V_WIND][:, i_index, j_index]
        return_param, _ = process_wind(u_wind, v_wind)

    elif parameter == 'WindSpeed':
        u_wind = ncdataset.variables[config.U_WIND][:, i_index, j_index]
        v_wind = ncdataset.variables[config.V_WIND][:, i_index, j_index]
        _, return_param = process_wind(u_wind, v_wind)

    elif parameter == 'PBLH':
        return_param = ncdataset.variables[config.PBLH][:, i_index, j_index]

    elif parameter == 'UST':
        return_param = ncdataset.variables[config.FRICTION_VELOCITY][:, i_index, j_index]

    elif parameter == 'LMO':
        friction_velocity = ncdataset.variables[config.FRICTION_VELOCITY][:, i_index, j_index]
        surface_pressure = ncdataset.variables[config.SURFACE_PRESSURE][:, i_index, j_index]
        surface_temperature = ncdataset.variables[config.SURFACE_TEMPERATURE][:, i_index, j_index]
        skin_temperature = ncdataset.variables[config.SKIN_TEMPERATURE][:, i_index, j_index]
        latent_heat = ncdataset.variables[config.LATENT_HEAT][:, i_index, j_index]
        sensible_heat = ncdataset.variables[config.SENSIBLE_HEAT][:, i_index, j_index]

        temperature_0 = skin_temperature * (surface_pressure / 101325.0) ** (-287.0 / 1005.0)
        mean_temperature = 0.5 * (temperature_0 + surface_temperature)
        evaporation = latent_heat / 2.5e9

        return_param = (
                - friction_velocity ** 3 * mean_temperature / (config.VON_KARMAN * config.G_ACCELL) /
                (sensible_heat + 0.608 * mean_temperature * evaporation)
        )

    elif parameter == 'SpecificHumidity':
        return_param = ncdataset.variables[config.SPECIFIC_HUMIDITY][:, 0, i_index, j_index]

    elif parameter == 'SurfaceTemperature':
        return_param = ncdataset.variables[config.SURFACE_TEMPERATURE][:, i_index, j_index]

    elif parameter == 'LiquidWaterContent':
        return_param = ncdataset.variables[config.CLOUD_MIXING_RATIO][:, 0, i_index, j_index]

    elif parameter == 'SolarRadiation':
        return_param = ncdataset.variables[config.SOLAR_RADIATION][:, i_index, j_index]

    elif parameter == 'Rain':
        convective_rain = ncdataset.variables[config.CONVECTIVE_RAIN][:, i_index, j_index]
        nonconvective_rain = ncdataset.variables[config.NON_CONVECTIVE_RAIN][:, i_index, j_index]
        total_rain = convective_rain + nonconvective_rain
        rain = np.zeros(total_rain.shape)
        rain[0] = total_rain[0]

        for i in range(1, rain.shape[0]):
            rain[i] = total_rain[i] - total_rain[i - 1]

        return_param = rain

    elif parameter == 'SurfacePressure':
        return_param = ncdataset.variables[config.SURFACE_PRESSURE][:, i_index, j_index]

    else:
        print(f'Wrong parameter name "{parameter}"')
        exit(1)

    return return_param


def upload_meteo_blob(city: str, filename: str, blob_key=config.AZURE_BLOB_KEY):
    """
    Uploads the meteo files to an Azure Storage Account to be accessed from outside.
    :param city:
    :param filename:
    :param blob_key:
    :return:
    """

    blob_service_client = BlobServiceClient.from_connection_string(blob_key)
    blob_name = filename.split('/')[-1]
    client = blob_service_client.get_blob_client(container=f'{city}-meteo', blob=blob_name)

    with open(file=filename, mode='rb') as blob_data:
        client.upload_blob(blob_data, overwrite=True)


def process_meteo_v2(domain, date_formatted=None, upload=False):
    """

    :param domain:
    :param date_formatted:
    :param upload:
    :return:
    """

    domain_dir = os.path.join(config.CHIMERE_OUTPUT_DIR, domain)
    meteo_dir = os.path.join(domain_dir, 'MUNICH/meteo')

    street_file = os.path.join(domain_dir, 'MUNICH/street.csv')
    streets = pd.read_csv(street_file)
    streets = db_to_street_center(streets)

    inter_file = os.path.join(domain_dir, 'MUNICH/intersection.csv')
    intersections = pd.read_csv(inter_file)

    N_streets, N_inters = len(streets), len(intersections)

    if not os.path.exists(meteo_dir):
        os.makedirs(meteo_dir)

    if not date_formatted:
        date_formatted = datetime.now().strftime('%Y-%m-%d') + '_00:00:00'
    else:
        date_formatted = date_formatted + '_00:00:00'

    raw_meteo_file = os.path.join(domain_dir, 'wrfout_d01_' + date_formatted)
    ncdataset = netCDF4.Dataset(raw_meteo_file)
    N_times = len(ncdataset.variables[config.TIMES][:])

    for street_param in STREET_PARAMETERS:
        param = np.zeros((N_streets, N_times))

        for i, st in streets.iterrows():
            street_lat, street_lon = st['center_lat'], st['center_lon']
            param[i, :] = get_param(street_param, street_lat, street_lon, ncdataset)
            filename = os.path.join(meteo_dir, f'{street_param}.bin')
            dumpBinary(param.astype(np.float32), filename)

        if upload:
            upload_meteo_blob(domain, filename)
            print(f'Uploaded file {filename.split("/")[-1]}')

    for inter_param in INTER_PARAMETERS:
        param = np.zeros((N_inters, N_times))

        for i, st in intersections.iterrows():
            street_lat, street_lon = st['lat'], st['lon']
            param[i, :] = get_param(inter_param, street_lat, street_lon, ncdataset)
            filename = os.path.join(meteo_dir, f'{inter_param}Inter.bin')
            dumpBinary(param.astype(np.float32), filename)

        if upload:
            upload_meteo_blob(domain, filename)
            print(f'Uploaded file {filename.split("/")[-1]}')


if __name__ == '__main__':
    process_meteo_v2('lindau', date_formatted='2023-10-16', upload=False)
