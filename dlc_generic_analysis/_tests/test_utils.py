from dlc_generic_analysis import utils
import numpy as np
import pandas
from numpy import testing


def test_scalar_dist():
    dist = utils.scalar_dist(np.array([10, 2]), np.array([2, 5]))
    np.testing.assert_array_almost_equal(8.54400374531753, dist)
    dist = utils.scalar_dist(np.array([10, 2]), np.array([2, 2]))
    np.testing.assert_array_equal(8, dist)
    dist = utils.scalar_dist(np.array([5, 3]), np.array([8, -2]))
    testing.assert_array_almost_equal(5.830951894845301, dist)


def test_dist():
    dist = utils.dist(np.array([[0, 1], [0, 2]]), np.array([[10, 10], [10, 25]]))
    testing.assert_array_almost_equal(
        np.array([13.45362404707371, 25.079872407968907], dtype=np.float_), dist
    )


def test_point_array():
    data = [[0, 1, 2], [3, 4, 5]]
    index = pandas.MultiIndex.from_product(
        [["Glab"], ["x", "y", "likelihood"]], names=["scorer", "coords"]
    )
    df = pandas.DataFrame(data, columns=index)
    print(df)
    arr = utils.point_array(df, ["Glab"])
    testing.assert_array_equal(arr, np.array([[0, 1], [3, 4]]))


def test_angle_between_lines():
    assert np.round(np.degrees(utils.angle_between_lines(np.sqrt(3), 0)), 6) == -60


def test_nan():
    nans = np.zeros((10, 10, 10), dtype=float)
    nans[:] = np.nan
    testing.assert_array_equal(utils.nan((10, 10, 10), dtype=float), nans)
