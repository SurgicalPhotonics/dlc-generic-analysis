from typing import Tuple, List
import numpy as np
from pandas import DataFrame


def dist(point1: Tuple[float, float], point2: Tuple[float, float]):
    return np.sqrt(np.abs(point2[0]-point1[0]) ** 2 + np.abs(point2[1]-point1[1]) ** 2)


def point_array(data_frame: DataFrame, points: List[str]):
    nd_arrays = list()
    for point in points:
        nd_arrays.append(data_frame[point].to_numpy(dtype=np.float64))
    return np.stack(nd_arrays, axis=0)[:, :, 0:2]

