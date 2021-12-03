"""Author: Frank Ma """
import numpy as np
from scipy import spatial


def regress(bp_points, frame):
    # print("Regressing frame", frame)
    x_arr = []
    y_arr = []
    ind_to_delete = np.array([], dtype=int)
    for i, bp in enumerate(bp_points):
        x_arr.append(bp["x"][frame])
        y_arr.append(bp["y"][frame])
        if bp["likelihood"][frame] < 0.99:
            ind_to_delete = np.append(ind_to_delete, i)

    for i in range(len(ind_to_delete)):
        ind_to_delete[i] = int(ind_to_delete[i])

    if ind_to_delete.size != 0:
        x_arr = np.delete(x_arr, ind_to_delete)
        y_arr = np.delete(y_arr, ind_to_delete)

    # If there is less than 3 points that we're confident about, return None
    if len(x_arr) < 3:
        return None

    m, b = np.polyfit(x_arr, y_arr, 1)
    return m, b


def distance(bp1, bp2, frame):
    p1 = (bp1["x"][frame], bp1["y"][frame])
    p2 = (bp2["x"][frame], bp2["y"][frame])

    d = spatial.distance.euclidean(p1, p2)
    return d


def interpolate_gaps(values, limit=None):
    """
    Fill gaps using linear interpolation, optionally only fill gaps up to a
    size of `limit`.
    https://stackoverflow.com/questions/36455083/working-with-nan-values-in-matplotlib
    """
    values = np.asarray(values)
    i = np.arange(values.size)
    valid = np.isfinite(values)
    filled = np.interp(i, i[valid], values[valid])

    if limit is not None:
        invalid = ~valid
        for n in range(1, limit + 1):
            invalid[:-n] &= invalid[n:]
        filled[invalid] = np.nan

    return filled
