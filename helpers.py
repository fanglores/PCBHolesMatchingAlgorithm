import numpy as np

SRC_IMG_NAME = 'photo_1.tif'
DST_IMG_NAME = 'photo_2.tif'

# Blue mask
blue_lower = np.array([254, 0, 0])
blue_upper = np.array([255, 0, 0])

# Red mask
red_lower = np.array([0, 0, 254])
red_upper = np.array([0, 0, 255])

def __get_closest_item_index(values_array, reference_value):
    distances = [np.linalg.norm(np.subtract(v, reference_value)) for v in values_array]
    return np.array(distances).argmin()

def get_index_of_closest_point(points, ref_point):
    return __get_closest_item_index(points, ref_point)

def get_corresponding_point_index(point_pairs: list, point: list):
    for i in range(len(point_pairs)):
        if (point_pairs[i] == point).all():
            return i
    raise ValueError(f'Didn`t find point {point}')

def get_triangles_pairs(paired_coordinates: list, vertexes1: list):
    vertexes1 = list(vertexes1)
    pairs = [vertexes1.copy(), []]

    for v in range(len(vertexes1)):
        new_vertexes2 = []
        for p in vertexes1[v]:
            ind = get_corresponding_point_index(paired_coordinates[0], p)
            new_vertexes2.append(paired_coordinates[1][ind])
        pairs[1].append(np.array(new_vertexes2).astype(np.float32))

    return pairs

