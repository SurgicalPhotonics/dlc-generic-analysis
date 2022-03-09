import os.path
from typing import List
import numpy as np
from pandas import DataFrame
import urllib.request
import tarfile
from numba import njit


@njit()
def dist(point0: np.ndarray, point1: np.ndarray):
    """
    calculates euclidian distance between 2 coordinates in a 2d space from an array
    exists because scipy.spatial.distance.euclidian is not elementwise
    :param point0: the first x,y coordinate
    :param point1: the second x,y coordinate
    :return:
    """
    return np.sqrt(
        np.power(np.abs(point1[:, 0] - point0[:, 0]), 2)
        + np.power(np.abs(point1[:, 1] - point0[:, 1]), 2)
    )


@njit
def scalar_dist(point0: np.ndarray, point1: np.ndarray):
    """
    calculates euclidian distance between 2 coordinates in a 2d space
    exists because scipy.spatial.distance.euclidian is not elementwise
    :param point0: the first x,y coordinate
    :param point1: the second x,y coordinate
    :return:
    """
    return np.sqrt(
        np.power(np.abs(point1[0] - point0[0]), 2) + np.power(np.abs(point1[1] - point0[1]), 2)
    )


def pd_distance(bp1: DataFrame, bp2: DataFrame, frame: int):
    """
    calculates the distance between DataFrame points

    """
    p1 = (bp1["x"][frame], bp1["y"][frame])
    p2 = (bp2["x"][frame], bp2["y"][frame])

    d = dist(p1, p2)
    return d


def point_array(data_frame: DataFrame, points: List[str], likelihood: bool = False):
    """
    returns a numpy array of the XY coordinates for the Listed points
    :param data_frame: the pandas dataframe from the h5 returned from deeplabcut's analysis
    :param points: a list of the names of the points to return coordinates for
    :param likelihood: if this is set True the likelihood value for each point will be included on the returned array
    """
    nd_arrays = list()
    if likelihood:
        for point in points:
            nd_arrays.append(data_frame[point][["x", "y", "likelihood"]].to_numpy(dtype=np.float_))
    else:
        for point in points:
            nd_arrays.append(data_frame[point][["x", "y"]].to_numpy(dtype=np.float_))
    return np.squeeze(np.stack(nd_arrays, axis=0))


def angle_between_lines(m1: float, m2: float) -> float:
    """
    calculates the angle between 2 lines in degrees
    :param m1: slope of line 1
    :param m2: slope of line 2
    :return: angle
    """
    return float(np.degrees(np.arctan(((m2 - m1) / (1 + m1 * m2)))))


def download_model(url: str, dest: str) -> str:
    """
    downloads a tarball model from url to dest/temp extracts it to dest/tar_name and returns the path of the
    model directory
    :param url: the url to download the model from
    :param dest: the destination to put the model
    :return: the path of the model directory
    """
    temp = os.path.join(dest, "temp")
    if not os.path.isdir(temp):
        os.mkdir(temp)
    model_tar = urllib.request.urlretrieve(url, temp)[0]
    if tarfile.is_tarfile(model_tar):
        ext = os.path.splitext(model_tar)[1]
        if ext == "gz" or ext == ".gz":
            tar = tarfile.open(model_tar, "r:gz")
        elif ext == "xz" or ext == ".xz":
            tar = tarfile.open(model_tar, "r:gz")
        else:
            raise ValueError("File must be .tar.gz or tar.xz")
    else:
        raise ValueError("File must be .tar.gz or tar.xz")
    name = os.path.splitext(os.path.split(model_tar)[1])[0]
    if not os.path.isdir(name):
        os.mkdir(name)
    tar.extractall(name)
    return name


def nan(shape, dtype: type = np.float_, order="C"):
    arr = np.zeros(shape=shape, dtype=dtype, order=order)
    arr[:] = np.nan
    return arr
