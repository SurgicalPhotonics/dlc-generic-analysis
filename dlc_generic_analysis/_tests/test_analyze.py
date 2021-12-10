import numpy as np

from dlc_generic_analysis.analysis import Analysis
import pandas


class ATest(Analysis):
    def __init__(self, h5, dlc_scorer):
        Analysis.__init__(self, h5, dlc_scorer)

    def analyze(self, video_path: str) -> (str, str):
        pass


def test_analyze():
    data = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    df = pandas.DataFrame(data, columns="b")
    df.to_hdf("test.h5", "a")
