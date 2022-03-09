from numba import njit
import numpy as np


nan_l = np.zeros(6)
nan_l[:] = np.nan


def nan_line():
    return nan_l.copy()


def from_slope(slope: np.ndarray, intercept: np.ndarray):
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


def from_points(end0, end1):
    if not end1[0] == end0[0]:
        slope = (end1[1] - end0[1]) / (end1[0] - end0[0])
    else:
        slope = 9e9
    return np.array(
        [slope, end0[1] - slope * end0[0], end0[0], end0[1], end1[0], end1[1]], dtype=np.float_
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
