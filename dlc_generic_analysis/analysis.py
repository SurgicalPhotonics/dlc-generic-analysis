import os
import pandas
from abc import ABC, abstractmethod


class Analysis(ABC):
    def __init__(self, h5_path, dlc_scorer, startframe=0, endframe=None):
        """
        Analysis:
        :param h5_path: the path of the h5 file created by analyze_videos
        :param dlc_scorer: the DeepLabCut model name
        :param startframe: the first frame of video to analyze
        :param endframe: the last frame of video to analyze
        """
        if not os.path.isfile(h5_path):
            raise FileNotFoundError(h5_path)
        self.df = pandas.read_hdf(h5_path)[dlc_scorer]
        self.start_frame = startframe
        if endframe is None:
            self.end_frame = len(self.df.index)
        else:
            self.end_frame = endframe
        assert self.end_frame > self.start_frame
        self.nframes = self.end_frame - self.start_frame

        self.outpath = os.path.split(h5_path)[0]
        self.outpath = os.path.join(h5_path, "analyzed_videos")

    @abstractmethod
    def analyze(self, video_path: str) -> (str, str):
        """

        :param video_path:
        :return: video_path, data_path: video_path: the path to the videof with analysis drawn on it.
        data_path: the path to the data generated from the analysis
        """


class ATest(Analysis):
    def __init__(self, h5, dlc_scorer):
        Analysis.__init__(self, h5, dlc_scorer)

    def analyze(self, video_path: str) -> (str, str):
        pass


if __name__ == "__main__":
    test = ATest(
        "/Users/louisadamian/Desktop/aemotrics/CompleteFlaccid1_trimmed_croppedDLC_resnet50_Aemotrics_V3Jan20shuffle1_600000.h5",
        "DLC_resnet50_Aemotrics_V3Jan20shuffle1_600000",
    )
    test.analyze("/Users/louisadamian/Desktop/aemotrics/CompleteFlaccid1.mp4")
