import json
from typing import List

import numpy as np
import pandas as pd
from scipy.spatial import Delaunay, Voronoi
from shapely import Point, Polygon

from munpy import config
from munpy.general import haversine_distance
from interpolation.map import Map
from interpolation.interpolacion import InterpolationPoint


def get_intersections(intersections_file):
    """

    :param intersections_file:
    :return:
    """

    with open(intersections_file, 'r') as inters:
        inter_lines = inters.readlines()

    intersections = pd.DataFrame()
    inter_ids = []
    lons, lats = [], []
    streets = []

    for line in inter_lines[1:]:
        line_content = line.split(';')
        inter_ids.append(int(line_content[0]))
        lons.append(float(line_content[1]))
        lats.append(float(line_content[2]))

        street_list = [int(s) for s in line_content[4:-1]]
        streets.append(street_list)

    intersections['inter_id'] = inter_ids
    intersections['lon'] = lons
    intersections['lat'] = lats
    intersections['streets'] = streets

    return intersections


def parse_polygon_geojson(points: np.ndarray, polygons: np.ndarray | List, filepath=None):
    """
    Crea un objeto GeoJSON con los simplex obtenidos de delaunay_traingulation o voronoi_diagram
    :param points: coordinates of the points forming the polygons
    :param polygons: indices of the points that form each polygon.
    :param filepath:
    :return:
    """

    features = []

    for index, polygon in enumerate(polygons):
        vertices = [points[s].tolist() for s in polygon]
        coordinates = [vertices + [vertices[0]]]

        feature = {
            'type': 'Feature',
            'properties': {
                'id': index + 1
            },
            'geometry': {
                'coordinates': coordinates,
                'type': 'Polygon'
            }
        }

        features.append(feature)

    geojs = {
        'type': 'FeatureCollection',
        'features': features
    }

    if filepath:
        with open(filepath, 'w') as gjs:
            json.dump(geojs, gjs)

    return geojs


def get_intersections_values(intersections: pd.DataFrame, streets: pd.DataFrame):
    """

    :param intersections: obtained from get_intersections
    :param streets: [street_id, NO2, NO, O3, ...]
    :return:
    """

    intersection_values = []

    for i, intersection in intersections.iterrows():  # todo: hacer esta operación para todas las columnas de 'streets'
        value = streets.loc[
            streets['street_id'].isin(intersection['streets']), config.NO2_COLUMN
        ]

        intersection_values.append(np.mean(value.to_numpy()))

    intersections[config.NO2_COLUMN] = intersection_values

    return intersections


def parse_node_values(intersections_with_values: pd.DataFrame):
    """
    Convierte el dataframe obtenido con get_intersections_values a un dict con
    el formato usado en el módulo de interpolación.
    :param intersections_with_values: obtenido con get_intersections_values
    :return: diccionario para rellenar la clase Nodes
    """

    node_values = {
        intersection['inter_id']: {
            'longitud': intersection['lon'],
            'latitud': intersection['lat'],
            config.NO2_COLUMN: intersection[config.NO2_COLUMN]
        } for _, intersection in intersections_with_values.iterrows()
    }

    return node_values


def delaunay_traingulation(intersections: pd.DataFrame):
    """

    :param intersections:
    :return:
    """

    points_array = np.array(
        [
            [intersection['lon'], intersection['lat']]
            for _, intersection in intersections.iterrows()
        ]
    )

    triangulation = Delaunay(points_array)

    return triangulation.points, triangulation.simplices


def find_outer_indices(points, diagram_center, max_distance):
    """

    :param max_distance:
    :param points:
    :param diagram_center:
    :return:
    """

    indices = []
    for i, p in enumerate(points[:-1]):
        dist = haversine_distance(p, diagram_center)
        if dist >= max_distance:
            indices.append(i)

    if haversine_distance(points[-1], diagram_center) >= max_distance:
        indices.append(-1)

    return indices


def voronoi_diagram(intersections: pd.DataFrame, max_distance=1600):
    """

    :param intersections:
    :param max_distance
    :return:
    """

    points_array = np.array(
        [
            [intersection['lon'], intersection['lat']]
            for _, intersection in intersections.iterrows()
        ]
    )

    voronoi = Voronoi(points_array)
    diagram_center = np.mean(voronoi.points, axis=0)
    out_indices = find_outer_indices(voronoi.vertices, diagram_center, max_distance)

    finite_regions = []
    for region in voronoi.regions:
        is_out = any(x in region for x in out_indices)
        if region and not is_out and -1 not in region:
            finite_regions.append(region)

    return voronoi.vertices, finite_regions


def identify_polygon_points(map: Map, vertices: np.ndarray, regions: List):
    """
    Encuentra qué puntos de una instancia de la clase Map están contenidos en cada región de un
    diagrama de Voronoi.

    :param map: np.ndarray([[lon, lat], [lon, lat], ...])
    :param vertices: scipy.spatial.Voronoi vertices attribute
    :param regions: scipy.spatial.Voronoi regions attribute después de eliminar los puntos no deseados
    :return: polygon_points --> List[List[int]]. Cada lista dentro de polygon_points contiene los
    ids de los punos de map que están dentro de cada región. Están en el mismo orden que el parámetro
    'regions'.
    """

    map_cells = map.cells.copy()
    polygon_points = []

    for i, region in enumerate(regions):
        polygon = Polygon(vertices[region])
        inside_list = []

        for grid_point in map_cells.copy():
            point = Point(
                [map.cells[grid_point]['lon'], map.cells[grid_point]['lat']]
            )

            if polygon.contains(point):
                inside_list.append(grid_point)
                map_cells.pop(grid_point)

        polygon_points.append(inside_list)

    return polygon_points


def interpolate_polygons(map, region_points, vertices, regions):
    """

    :param map:
    :param region_points:
    :param vertices:
    :param regions:
    :return:
    """

    for i, (region, points) in enumerate(zip(regions, region_points)):
        region_vertices = vertices[region]

        interpolation_params = {
            i: {
                'lon': vertex[0], 'lat': vertex[1],
            }
        }
        interp = InterpolationPoint()


if __name__ == '__main__':
    import os
    from munpy.postprocessing.postprocessing import extract_city
    from interpolation.generar_geoJSON import generar_geoJSON

    city = 'lindau'
    city_dir = os.path.join(config.LEZ_DIR, city)
    inter_filename = os.path.join(city_dir, 'intersection.dat')

    # Generar cuadrícula y mapa
    min_lat, min_lon, max_lat, max_lon = 47.5502, 9.6799, 47.5619, 9.6999
    resolution = 30  # metros
    lindau_gjs = generar_geoJSON(resolution, min_lon, max_lon, max_lat, min_lat)
    mapa = Map(lindau_gjs, {})

    # generar diagrama de voronoi y guardaro en geojson
    _, base_simulation, _ = extract_city(
        city, config.URL, config.DATABASE, config.USER,
        config.PASSWORD, config.PORT
    )

    inters = get_intersections(inter_filename)
    inters = get_intersections_values(inters, base_simulation)
    verts, regs = voronoi_diagram(inters)

    reg_points = identify_polygon_points(mapa.cells, verts, regs)

    points_1st_region = {
        k: mapa.cells[k] for k in reg_points[0]
    }

    features = []
    for point in points_1st_region:
        coordinates = [points_1st_region[point]['lon'], points_1st_region[point]['lat']]
        feature = {
            'type': 'Feature',
            'properties': {
                'id': point
            },
            'geometry': {
                'coordinates': coordinates,
                'type': 'Point'
            }
        }

        features.append(feature)

    hahahahahahaha = {
        'type': 'FeatureCollection',
        'features': features
    }
    with open(os.path.join(city_dir, 'region_1.geojson'), 'w') as j:
        json.dump(hahahahahahaha, j)
