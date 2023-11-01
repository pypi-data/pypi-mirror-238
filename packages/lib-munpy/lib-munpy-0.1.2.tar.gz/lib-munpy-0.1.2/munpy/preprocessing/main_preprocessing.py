import datetime
import os

import numpy as np
import pandas as pd

from munpy import config
from munpy.general import readBinary, dumpBinary, reshape, generalized_normal
from munpy.copert.emissions import calculate_traffic_emissions
from munpy.preprocessing.background import process_background_v2
from munpy.preprocessing.meteo import process_meteo_v2


if __name__ == '__main__':
    city = 'cartagena'
    VERBOSE = False

    latitud_ctg = 37.6048
    longitud_ctg = -0.9861

    latitud_lindau = 47.55
    longitud_lindau = 9.69

    N_times = 48
    streets_df = pd.read_csv(
        os.path.join(config.LEZ_DIR, f'{city}/street.csv')
    )
    intersections_df = pd.read_csv(
        os.path.join(config.LEZ_DIR, f'{city}/intersection.csv')
    )

    N_street = len(streets_df)
    N_inter = len(intersections_df)

    # EMISIONES
    city_dir = os.path.join(config.LEZ_DIR, city)
    traffic_file = os.path.join(city_dir, 'base_traffic.csv')
    traffic = pd.read_csv(traffic_file)
    traffic.rename(columns={'id': 'street_id'}, inplace=True)
    emission = calculate_traffic_emissions(traffic)

    for gas in emission.columns:
        gas_emission = emission[gas].to_numpy() * 1e6  # valor de cada calle en micro gramos
        gas_emission = reshape(gas_emission, N_times=N_times, mode='time')

        for ts in range(N_times):
            # Simulation starts at 6 AM, peak hours are 12 AM to 6 PM
            gas_emission[ts, :] = gas_emission[ts, :] * (
                generalized_normal(ts, mu=6, sigma=6, beta=8) + generalized_normal(ts, mu=30, sigma=6, beta=8)
            ) + 0.05 * np.abs(np.random.normal(loc=np.mean(gas_emission), size=N_street))

        filename = os.path.join(config.LEZ_DIR, f'{city}/emission/{gas.upper()}.bin')
        dumpBinary(gas_emission, filename)

    # BACKGROUND
    process_background_v2(city, config.API_KEY)

    # METEO
    process_meteo_v2(city, N_street, N_inter, latitud_lindau, longitud_lindau, date_formatted='2023-10-16')
