from dlc_generic_analysis import line
import numpy as np
from numpy import testing


def test_nan_line():
    testing.assert_array_equal(line.nan_line(), np.array([np.nan] * 6, dtype=np.float_))


def test_from_slope():
    test_line = line.from_slope(2, 0)
    l = np.array([2, 0, 0, 0, 1, 2], dtype=np.float_)
    testing.assert_array_equal(test_line, l)


def test_from_points_1d():
    test_line = line.from_points_1d((1, 2), (10, 20))
    np_line = np.array([2, 0, 1, 2, 10, 20], dtype=np.float_)
    print(np_line)
    testing.assert_array_equal(test_line, np_line)


def test_from_points():
    test_lines = line.from_points(np.array([[10, 1], [5, 5]]), np.array([[20, 2], [10, 0]]))
    np_lines = np.array([[0.1, 0, 10, 1, 20, 2], [-1, 10, 5, 5, 10, 0]])
    testing.assert_array_equal(np_lines, test_lines)


def test_get_slope():
    np_line = np.array([2, 0, 1, 2, 10, 20], dtype=np.float_)
    assert line.slope(np_line) == 2


def test_get_intercept():
    np_line = np.array([2, 0, 1, 2, 10, 20], dtype=np.float_)
    assert line.intercept(np_line) == 0


def test_get_end0():
    np_line = np.array([2, 0, 1, 2, 10, 20], dtype=np.float_)
    testing.assert_array_equal(line.end0(np_line), np.array([1, 2]))


def test_get_end1():
    np_line = np.array([2, 0, 1, 2, 10, 20], dtype=np.float_)
    testing.assert_array_equal(line.end1(np_line), np.array([10, 20]))
