from interpolation.generar_geoJSON import generar_geoJSON
from interpolation.map import Map
from interpolation.nodes import Nodes


min_lat, min_lon, max_lat, max_lon = 47.5502, 9.6799, 47.5619, 9.6999
resolution = 10  # metros
lindau_gjs = generar_geoJSON(resolution, min_lon, max_lon, max_lat, min_lat)


