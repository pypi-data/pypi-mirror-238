import json
import numpy as np
import pandas as pd


def dat_to_db(streets: pd.DataFrame, intersections: pd.DataFrame):
    """
    Converts the content of streets to format of crate database.

    :param streets: DataFrame loaded from 'street.dat'
    :param intersections: DataFrame lodaded from the raw intersections
    file, that only contains an intersectoin id and its coordinates.

    :return: DataFrame with street_id and a LineString of its coordinates.
    """

    ids, coordinates = [], []
    for _, street in streets.iterrows():
        ids.append(int(street["id"]))
        first_inter = int(street["begin_inter"])
        second_inter = int(street["end_inter"])

        coords_ini = intersections.loc[
            intersections["id"] == first_inter, ['lon', 'lat']
        ].to_numpy()[0]

        coords_fin = intersections.loc[
            intersections["id"] == second_inter, ['lon', 'lat']
        ].to_numpy()[0]

        coordinates.append([list(coords_ini), list(coords_fin)])

    return pd.DataFrame({'street_id': ids, 'coordinates': coordinates})


def dat_to_street_center(streets: pd.DataFrame, intersections: pd.DataFrame):
    """
    Genera e archivo all_streets.csv, que contiene street_id y centro de las coordenadas
    :param streets: load(street.dat)
    :param intersections: load(raw_intersection.dat))
    :return:
    """

    street_dataframe = dat_to_db(streets, intersections)
    center_lat = [
        np.mean(coords, axis=0)[0]
        for coords in street_dataframe['coordinates']
    ]
    center_lon = [
        np.mean(coords, axis=0)[1]
        for coords in street_dataframe['coordinates']
    ]

    street_dataframe['lat'] = center_lat
    street_dataframe['lon'] = center_lon

    return street_dataframe


def db_to_street_center(streets: pd.DataFrame):
    """
    Añade una columna con el centro de la calle al csv de calles. Exactamente igual que
    dat_to_street_center pero empezando desde el formato database.
    :param streets:
    :return:
    """

    center_lat = [
        np.mean(json.loads(coords), axis=0)[1]
        for coords in streets['coordinates']
    ]
    center_lon = [
        np.mean(json.loads(coords), axis=0)[0]
        for coords in streets['coordinates']
    ]

    streets['center_lat'] = center_lat
    streets['center_lon'] = center_lon

    return streets


def dat_to_geojson(streets: pd.DataFrame, intersections: pd.DataFrame, color=None):
    """
    Genera un geojson de calles a partir del dataframe.
    :param streets:
    :param intersections:
    :param color: color con el que pintar las calles, ej: #ff0000 rojo puro
    :return:
    """

    streets = dat_to_db(streets, intersections)

    features = []
    for _, street in streets.iterrows():
        # GeoJSON lee por defecto las coordenadas en [longitud, latitud]
        coords = street['coordinates']

        feature = {
            "type": "Feature",
            "properties": {
                "id": str(street['street_id'])
            },
            "geometry": {
                "coordinates": coords,
                "type": "LineString"
            }
        }

        if color:
            feature['properties']["stroke"] = color

        features.append(feature)

    geojs = {"type": "FeatureCollection", "features": features}

    return geojs


if __name__ == '__main__':
    import os
    from munpy import config

    city = 'lindau'
    city_dir = os.path.join(config.LEZ_DIR, city)

    street = pd.read_csv(
        os.path.join(city_dir, 'street.dat'), sep=';'
    )
    street.rename(columns={'#id': 'id'}, inplace=True)

    intersection = pd.read_csv(os.path.join(city_dir, 'intersection.csv'))

    street_db = dat_to_db(street, intersection)
    street_db.to_csv(os.path.join(city_dir, 'street.csv'), index=False)

    geojs = dat_to_geojson(street, intersection, color='#ff0000')
    with open(os.path.join(city_dir, 'street.geojson'), 'w') as j:
        json.dump(geojs, j)
