from dlc_generic_analysis import utils
import numpy as np
import pytest
import pandas


def test_dist():
    dist = utils.dist((0, 0), (1, 2))
    assert np.sqrt(1 + 2 ** 2) == pytest.approx(dist)


def test_point_array():
    data = [[0, 1, 2], [3, 4, 5]]
    df = pandas.DataFrame(data, columns=["a", "b", "c"])
    print(df)
    arr = utils.point_array(df, ["a"])
    np.array_equal(arr, np.array([[0, 3]]))


def test_angle_between_lines():
    assert np.round(utils.angle_between_lines(np.sqrt(3), 0), 6) == -60


#  testing video manipulation functions is too expensive
