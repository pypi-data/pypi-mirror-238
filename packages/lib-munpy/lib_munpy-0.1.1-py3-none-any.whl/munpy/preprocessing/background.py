import os

import numpy as np
import pandas as pd

import cdsapi
from datetime import datetime
import yaml
from netCDF4 import Dataset

from munpy.io import dumpBinary
from munpy.general import get_nc_index, reshape
from munpy.preprocessing.format import db_to_street_center
from munpy import config


def download_data(
    key_path, save_path,
    latitude, longitude,
    download_date=None, leadtime_hours=48
):
    """

    :param latitude:
    :param longitude:
    :param key_path:
    :param save_path:
    :param download_date: if None, aplica fecha de ejecución
    :param leadtime_hours:
    :return:
    """

    max_lat, min_lat = latitude + 0.5, latitude - 0.5
    max_lon, min_lon = longitude + 0.5, longitude - 0.5

    if not download_date:
        download_date = datetime.now().strftime('%Y-%m-%d')

    download_filename = os.path.join(save_path, 'copernicus_forecast.nc')

    # Load authentication credentials from the provided YAML file
    with open(key_path, 'r') as auth_file:
        credentials = yaml.safe_load(auth_file)

    c = cdsapi.Client(url=credentials['url'], key=credentials['key'])

    c.retrieve(
        'cams-europe-air-quality-forecasts',
        {
            'variable': [
                'ammonia', 'carbon_monoxide', 'formaldehyde', 'sulphur_dioxide',
                'nitrogen_dioxide', 'nitrogen_monoxide', 'ozone',
                'particulate_matter_10um', 'particulate_matter_2.5um',
            ],
            'model': 'ensemble',
            'level': '0',
            'date': f'{download_date}/{download_date}',
            'type': 'forecast',
            'time': '00:00',
            'leadtime_hour': [str(i) for i in range(leadtime_hours)],
            'area': [
                max_lat, min_lon,
                min_lat, max_lon,
            ],
            'format': 'netcdf',
        },
        download_filename
    )

    return download_filename


def process_background(
    city, N_streets, key_path,
    latitude, longitude, date=None
):
    """

    :param city:
    :param N_streets:
    :param key_path:
    :param latitude:
    :param longitude:
    :param date:
    :return:
    """

    city_dir = os.path.join(config.LEZ_DIR, city)
    background_dir = os.path.join(city_dir, 'background')

    if not os.path.exists(background_dir):
        os.makedirs(background_dir)

    ncfile = download_data(key_path, background_dir, latitude, longitude, date)
    dataset = Dataset(ncfile, mode='r')
    i_index, j_index, _ = get_nc_index(latitude, longitude, dataset, mode='copernicus')

    background_pollutants = [
        'co_conc', 'nh3_conc', 'no2_conc', 'no_conc',
        'o3_conc', 'pm10_conc', 'pm2p5_conc'
    ]

    munich_pollutant_names = [
        'CO', 'NH3', 'NO2', 'NO', 'O3', 'PM10', 'PM25'
    ]

    time_values = {
        munich_var: dataset.variables[var][:, 0, i_index, j_index]
        for var, munich_var in zip(background_pollutants, munich_pollutant_names)
    }

    for pollutant in time_values:
        reshaped_pollutant = reshape(time_values[pollutant], N_streets=N_streets)
        dumpBinary(
            reshaped_pollutant, os.path.join(background_dir, pollutant+'.bin')
        )


def process_background_v2(city, key_path, date=None, leadtime_hours=48):
    city_dir = os.path.join(config.LEZ_DIR, city)
    street_file = os.path.join(city_dir, 'domain/street.csv')
    background_dir = os.path.join(city_dir, 'background_test')

    if not os.path.exists(background_dir):
        os.makedirs(background_dir)

    streets = pd.read_csv(street_file)
    streets = db_to_street_center(streets)
    N_streets = len(streets)
    mean_latitude, mean_longitude = streets[['center_lat', 'center_lon']].mean().values

    ncfile = download_data(key_path, background_dir, mean_latitude, mean_longitude, date)
    dataset = Dataset(ncfile, mode='r')

    gases = {
        'co_conc': 'CO', 'nh3_conc': 'NH3', 'no2_conc': 'NO2',
        'no_conc': 'NO', 'o3_conc': 'O3',
        'pm10_conc': 'PM10', 'pm2p5_conc': 'PM25'
    }

    for gas in gases:
        gas_array = np.zeros((N_streets, leadtime_hours))

        for i, st in streets.iterrows():
            center_lat, center_lon = st['center_lat'], st['center_lon']
            i_index, j_index, _ = get_nc_index(center_lat, center_lon, dataset, mode='copernicus')
            gas_street_values = dataset.variables[gas][:, 0, i_index, j_index]
            gas_array[i, :] = gas_street_values

        dumpBinary(gas_array, os.path.join(background_dir, f'{gases[gas]}.bin'))


if __name__ == "__main__":
    # process_background('lindau', 188, config.API_KEY, latitude=47.55, longitude=9.69)
    process_background_v2('lindau', config.API_KEY)
