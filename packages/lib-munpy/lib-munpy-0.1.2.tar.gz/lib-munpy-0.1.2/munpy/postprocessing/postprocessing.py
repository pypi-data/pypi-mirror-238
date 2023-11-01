import json
import os.path

import numpy as np
import pandas as pd
from itertools import chain


from munpy.general import readBinary, haversine_distance
from munpy.general import connect, postgresql_to_dataframe, sql_connection
from munpy import config

from munpy.copert.emissions import calculate_traffic_emissions

"""
1. Extraer datos de tráfico de BBDD -> csv_traffic, base_simulation: DANI
2. Aplicar fórmula (desarrollar) de reducciones a csv_traffic -> traffic_reduction (%): NOEL
3. Pasar traffic_reduced por Pollemission -> emission_reduction (%): DANI
4. Traducir emission_reduction a concentration_reduction (%): NOEL
5. Aplicar concentration_redcution a csv_concentration: NOEL
"""


def get_all_streets(city, connection):
    """

    :param connection:
    :param city:
    :return:
    """

    select_query = f"""SELECT * FROM {city}.{config.STREET_COORDINATES_TABLE}"""
    all_streets = postgresql_to_dataframe(connection, select_query)

    center_lon, center_lat = [], []
    for _, street in all_streets.iterrows():
        coordinates = json.loads(street['coordinates'])
        center_lon.append(np.mean(coordinates, axis=0)[0])
        center_lat.append(np.mean(coordinates, axis=0)[1])

    all_streets['center_lat'] = center_lat
    all_streets['center_lon'] = center_lon

    return all_streets


def get_base_simulation(city, connection):
    """

    :param connection:
    :param city:
    :return:
    """

    select_query = f"""SELECT * FROM {city}.{config.BASE_SIMULATION_TABLE}"""
    base_simulation = postgresql_to_dataframe(connection, select_query)

    return base_simulation


def get_base_traffic(city, connection):
    """

    :param connection:
    :param city:
    :return:
    """

    select_query = f"""SELECT * FROM {city}.{config.BASE_TRAFFIC_TABLE}"""
    base_traffic = postgresql_to_dataframe(connection, select_query)

    return base_traffic


def extract_city(city, db_url, db_name, db_user, db_password, db_port):
    """
    Extrae los datos de tráfico y de calles de la base de datos con esquema 'city'

    :param city:
    :param db_url:
    :param db_name:
    :param db_port:
    :param db_user:
    :param db_password:
    :return:
    """

    conn = connect(db_url, db_name, db_user, db_password, db_port)
    raw_streets = get_all_streets(city, conn)
    base_simulation = get_base_simulation(city, conn)
    base_traffic = get_base_traffic(city, conn)

    conn.close()

    return raw_streets, base_simulation, base_traffic


def bulk_load_simulation(
    simulation: pd.DataFrame, city, db_url, db_name,
    db_user, db_password, db_port, mode='custom'
):
    """

    :param simulation:
    :param city:
    :param mode:
    :param db_url:
    :param db_name:
    :param db_user:
    :param db_password:
    :param db_port:
    :return:
    """

    engine = sql_connection(db_url, db_name, db_user, db_password, port=db_port)

    name = config.CUSTOM_SIMULATION_TABLE
    if mode == 'base':
        name = config.BASE_SIMULATION_TABLE

    simulation.to_sql(name, engine, schema=city, if_exists='replace', index=False)


def bulk_load_streets(
    street_coordinates: pd.DataFrame, city, db_url,
    db_name, db_user, db_password, db_port
):
    """

    :param street_coordinates:
    :param city:
    :param db_url:
    :param db_name:
    :param db_port:
    :param db_user:
    :param db_password:
    :return:
    """

    engine = sql_connection(db_url, db_name, db_user, db_password, port=db_port)
    name = config.STREET_COORDINATES_TABLE
    street_coordinates.to_sql(name, engine, schema=city, if_exists='replace', index=False)


def bulk_load_traffic(
    base_traffic: pd.DataFrame, city, db_url,
    db_name, db_user, db_password, db_port
):
    """

    :param base_traffic:
    :param city:
    :param db_url:
    :param db_name:
    :param db_user:
    :param db_password:
    :param db_port:
    :return:
    """

    engine = sql_connection(db_url, db_name, db_user, db_password, port=db_port)
    name = config.BASE_TRAFFIC_TABLE
    base_traffic.to_sql(name, engine, schema=city, if_exists='replace', index=False)


def get_nearby_streets(lez_streets_list, all_streets: pd.DataFrame, max_dist=100.0):
    """
    Calcula qué calles se ven afectadas indirectamente por la LEZ en función a la distancia existente
    con las calles donde se aplica una modificación directa. Para ello necesita un DataFrame 'all_streets'
    que contenga todas las calles con las coordenadas de su centro, de forma que se calcula la distancia
    entre una calle LEZ y una secundaria. Si esta distancia es menos que 'max_dist', se entiende que
    la reducción del tráfico en la calle LEZ aumentará indirectamente el tráfico en la calle secundaria.

    :param lez_streets_list:
    :param all_streets:
    :param max_dist:
    :return:
    """

    nearby_streets = {street_id: [] for street_id in lez_streets_list}  # diccionario con las calles adyacentes

    for street_id in lez_streets_list:
        main_coords = all_streets.loc[  # coordenadas de la calle LEZ
            all_streets['street_id'] == street_id, ['center_lat', 'center_lon']
        ].to_numpy()[0]

        for second_street in all_streets['street_id']:
            second_coords = all_streets.loc[
                all_streets['street_id'] == second_street, ['center_lat', 'center_lon']
            ].to_numpy()[0]

            distance = haversine_distance(main_coords, second_coords)

            if distance < max_dist:
                nearby_streets[street_id].append(second_street)

    nearby_streets = list(  # Juntar todas las afectadas en una única lista eliminando los duplicados
        set(
            chain(*[nearby_streets[st] for st in nearby_streets])
        )
    )

    nearby_streets = [  # eliminar las calles que estén en la LEZ
        st for st in nearby_streets
        if st not in lez_streets_list
    ]

    return nearby_streets


def calculate_traffic_impact(lez_reductions, lez_reductions_file=config.LEZ_REDUCTIONS_FILE):
    """

    :param lez_reductions:
    :param lez_reductions_file:
    :return:
    """

    with open(lez_reductions_file, 'r') as j:
        reductions_template = json.load(j)

    individual_impact = [reductions_template[value] for value in lez_reductions]  # porcentajes de reducción

    # Reducciones
    if 1 in individual_impact:
        total_reduction = 0.0
    else:
        total_reduction = 1.0 - np.tanh(0.6 * sum(individual_impact))

    # Aumentos
    total_increment = 1 - total_reduction

    return total_reduction, total_increment


def apply_traffic_impact(base_traffic: pd.DataFrame, lez_streets, secondary_streets, lez_reductions):
    """
    Calcula las reducciones al tráfico base en función de la petición http.

    :param base_traffic:
    :param lez_streets:
    :param secondary_streets:
    :param lez_reductions:

    :return:
    """

    traffic_reduction, traffic_increment = calculate_traffic_impact(lez_reductions)
    print(traffic_reduction, traffic_increment)

    reduced_traffic = base_traffic.copy()
    reduced_traffic['volume'] = reduced_traffic['volume'].astype(np.float64)

    reduced_traffic.loc[
        reduced_traffic['street_id'].isin(lez_streets), 'volume'
    ] *= traffic_reduction

    reduced_traffic.loc[
        reduced_traffic['street_id'].isin(secondary_streets), 'volume'
    ] *= 1 + traffic_increment / (1 + len(secondary_streets))

    return reduced_traffic


def postprocess(city, lez_streets, lez_reductions):
    """
    Procesa los resultados de la simulación base en función de las medidas y las
    calles que llegan de la petición http.

    :param city:
    :param lez_streets:
    :param lez_reductions:
    :return:
    """

    streets, base_simulation, base_traffic = extract_city(
        city, config.URL, config.DATABASE, config.USER,
        config.PASSWORD, config.PORT
        )

    secondary_streets = get_nearby_streets(lez_streets, streets)
    reduced_traffic = apply_traffic_impact(base_traffic, lez_streets, secondary_streets, lez_reductions)

    base_emission = calculate_traffic_emissions(base_traffic) * 1.0e6
    reduced_emission = calculate_traffic_emissions(reduced_traffic) * 1.0e6

    gas_columns = list(base_emission.columns)
    gas_columns.remove('street_id')

    lez_simulation = base_simulation.copy()

    for gas in [
        config.CO_COLUMN, config.NO_COLUMN, config.NO2_COLUMN,
        config.PM10_COLUMN, config.PM25_COLUMN, config.O3_COLUMN
    ]:
        if gas == config.O3_COLUMN:
            pass

        else:
            ratio_concentration_emission = base_simulation[gas] / base_emission[gas]
            lez_simulation[gas] = reduced_emission[gas] * ratio_concentration_emission

    # bulk_load_simulation(
    #     lez_simulation, city, config.URL, config.DATABASE,
    #     config.USER, config.PASSWORD, config.PORT
    # )

    return base_simulation, lez_simulation


def get_munich_results(city, upload=False, verbose=False):
    """

    :param city: folder where binary result files are being stored.
    :param upload: if True, data is upload to database
    :param verbose: if True, prints results dataframe for observation.
    :return:
    """

    city_dir = os.path.join(config.LEZ_DIR, city)
    result_dir = os.path.join(city_dir, 'results')
    background_dir = os.path.join(city_dir, 'background')
    emission_dir = os.path.join(city_dir, 'emission')
    street_file = os.path.join(city_dir, 'domain/street.csv')

    street = pd.read_csv(street_file)
    N_street = len(street)

    results_dataframe = pd.DataFrame()
    results_dataframe['street_id'] = street['street_id']

    for gas in [config.CO_COLUMN, config.NO2_COLUMN, config.NO_COLUMN, config.O3_COLUMN]:
        gas_filename = os.path.join(result_dir, f'{gas.upper()}.bin')
        gas_results = readBinary(gas_filename, N_street)[36, :]  # timestamp 36 --> 12 AM, all streets
        results_dataframe[gas] = gas_results

    for pm in [config.PM10_COLUMN, config.PM25_COLUMN]:
        pm_background = readBinary(os.path.join(background_dir, f'{pm.upper()}.bin'), N_street)
        pm_emission = readBinary(os.path.join(emission_dir, f'{pm.upper()}.bin'), N_street)
        pm_result = pm_background + pm_emission / np.mean(pm_emission)
        results_dataframe[pm] = pm_result[36, :]

    if upload:
        bulk_load_simulation(
            results_dataframe, city, config.URL, config.DATABASE,
            config.USER, config.PASSWORD, config.PORT, mode='base'
        )

    if verbose:
        print(results_dataframe.head(n=10))

    return results_dataframe
