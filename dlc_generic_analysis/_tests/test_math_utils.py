import numpy as np
from dlc_generic_analysis import math_utils


def test_interpolate_gaps():
    values = [1, 3, 5, 7, 9]
    filled = math_utils.interpolate_gaps(values, 5)
    print(filled)
    assert np.array_equal(np.array([1, 3, 5, 7, 9]), filled)
