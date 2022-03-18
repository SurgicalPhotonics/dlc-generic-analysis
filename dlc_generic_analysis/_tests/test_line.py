from dlc_generic_analysis import line
import numpy as np
from numpy import testing


def test_nan_line():
    testing.assert_array_equal(line.nan_line(), np.array([np.nan] * 6, dtype=np.float_))


def test_from_slope():
    test_line = line.from_slope(2, 0)
    l = np.array([2, 0, 0, 0, 1, 2], dtype=np.float_)
    testing.assert_array_equal(test_line, l)


def test_from_points():
    test_line = line.from_points((1, 2), (10, 20))
    l = np.array([2, 0, 1, 2, 10, 20], dtype=np.float_)
    testing.assert_array_equal(test_line, l)
