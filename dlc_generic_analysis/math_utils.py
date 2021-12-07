"""Author: Frank Ma """
import numpy as np
from scipy import spatial


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
