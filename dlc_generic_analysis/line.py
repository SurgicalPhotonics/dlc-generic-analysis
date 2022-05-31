from numba import njit
import numpy as np


nan_l = np.zeros(6)
nan_l[:] = np.nan


def nan_line():
    return nan_l.copy()


def from_slope(slope: np.ndarray, intercept: np.ndarray):
    slope = np.array(slope)
    intercept = np.array(intercept)
    if len(slope.shape) > 0:
        if slope.shape[0] >= 1:
            axis = 1
        else:
            axis = 0
    else:
        axis = 0
    return np.stack(
        [
            slope,
            intercept,
            np.zeros(slope.shape),
            intercept,
            np.ones(slope.shape),
            np.round_(intercept + slope),
        ],
        axis=axis,
    )


def from_points_1d(end0, end1):
    """
    creates a numpy array representation of a line from 2 points
    :param end0: the first point
    :param end1: the second point
    """
    slope = (end1[1] - end0[1]) / (end1[0] - end0[0])
    return np.stack(
        [
            slope,
            end0[1] - slope * end0[0],
            end0[0],
            end0[1],
            end1[0],
            end1[1],
        ]
    )


def from_points(end0, end1):
    """
    creates a list of lines from 2 2d lists of points
    :param end0: a list of the first points
    :param end1: a list of the second points
    """
    slope = (end1[:, 1] - end0[:, 1]) / (end1[:, 0] - end0[:, 0])
    return np.stack(
        [
            slope,
            end0[:, 1] - slope * end0[:, 0],
            end0[:, 0],
            end0[:, 1],
            end1[:, 0],
            end1[:, 1],
        ],
        axis=1,
    )


@njit()
def set_ends(line: np.ndarray, points: "np.ndarray") -> "np.ndarray":
    """
    sets the ends of a line to the outermost points
    :param line:
    :param points:
    :return:
    """
    c = points[np.logical_not(np.isnan(points).any(axis=1))]
    y = c[points.shape[0] - 1, 1]
    if line[0] != 0:
        line[4] = int((y - line[1]) / line[0])
        line[5] = int(y)
    else:
        line[4] = 1
        line[5] = int(y)
    y = c[0][1]
    if line[0] != 0:
        line[2] = int((y - line[1]) / line[0])
        line[3] = int(y)
    else:
        line[2] = 1
        line[3] = int(y)
    return line


def slope(line: np.ndarray):
    return line[0]


def intercept(line: np.ndarray):
    return line[1]


def end0(line: np.ndarray):
    return line[2:4]


def end1(line: np.ndarray):
    return line[4:6]
