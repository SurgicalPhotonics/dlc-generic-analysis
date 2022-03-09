from dlc_generic_analysis import utils
import numpy as np
import pandas


def test_distance():
    data = [[0, 1, 2], [7, 5, 3]]
    data1 = [[6, 3, 9], [8, 4, 3]]
    bp1 = pandas.DataFrame(data, columns=["x", "y", "confidence"], dtype=np.float_)
    bp2 = pandas.DataFrame(data1, columns=["x", "y", "confidence"])
    dist = utils.pd_distance(bp1, bp2, 1)
    print(f"dist = {dist}")
    assert dist == np.sqrt(2)


def test_point_array():
    data = [[0, 1, 2], [3, 4, 5]]
    index = pandas.MultiIndex.from_product(
        [["Glab"], ["x", "y", "likelihood"]], names=["scorer", "coords"]
    )
    df = pandas.DataFrame(data, columns=index)
    print(df)
    arr = utils.point_array(df, ["Glab"])
    np.array_equal(arr, np.array([[0, 3]]))


def test_angle_between_lines():
    assert np.round(utils.angle_between_lines(np.sqrt(3), 0), 6) == -60


#  testing video manipulation functions is too expensive
