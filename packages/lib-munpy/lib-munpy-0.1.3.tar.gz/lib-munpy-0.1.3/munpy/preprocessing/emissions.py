import os.path

import numpy as np
import pandas as pd

from munpy.general import dumpBinary, generalized_normal
from munpy.copert.emissions import calculate_traffic_emissions
from munpy import config


def process_emission_v2(city, N_times=48, save=False):
    """

    :param city:
    :param N_times:
    :param save:
    :return:
    """
    city_dir = os.path.join(config.LEZ_DIR, city)
    emission_dir = os.path.join(city_dir, 'emission')

    traffic_file = os.path.join(city_dir, 'base_traffic.csv')
    base_traffic = pd.read_csv(traffic_file)
    emission = calculate_traffic_emissions(base_traffic) * 1e6  # Pasar de gramos a microgramos

    if not os.path.exists(emission_dir):
        os.makedirs(emission_dir)

    for gas in [
        config.CO_COLUMN, config.NO2_COLUMN, config.NO_COLUMN,
        config.PM10_COLUMN, config.PM25_COLUMN
    ]:
        gas_emission = np.zeros((N_times, len(emission)))

        for k in range(N_times):
            # gas_emission[k, :] = (emission[gas] +
            #                       0.2 * emission[gas].mean() * generalized_normal(k, mu=12, sigma=8, beta=8) +
            #                       0.2 * emission[gas].mean() * generalized_normal(k, mu=36, sigma=8, beta=8))
            gas_emission[k, :] = emission[gas] * (
                generalized_normal(k, mu=12, sigma=8, beta=8) + generalized_normal(k, mu=36, sigma=8, beta=8)
            )

        if save:
            dumpBinary(gas_emission, os.path.join(emission_dir, f'{gas.upper()}.bin'))


if __name__ == '__main__':
    process_emission_v2('lindau', save=True)
