import os
import pandas
import tqdm
import numpy as np
from abc import ABC, abstractmethod
import utils
from matplotlib import pyplot as plt


class Analysis(ABC):
    def __init__(self, h5_path, dlc_scorer, startframe=0, endframe=None):
        """
        Analysis:
        :param h5_path: the path of the h5 file created by analyze_videos
        :param dlc_scorer: the DeepLabCut model name
        :param startframe: the first frame of video to analyze
        :param endframe: the last frame of video to analyze
        """
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
        self.datastore = dict()

    def get(self, name):
        if name in self.datastore:
            return self.datastore[name]

    def duplicate_name_check(self, name):
        if name in self.datastore:
            raise RuntimeError(name + " has already been defined.")

    def calc_regression_line(self, name: str, bps):
        """
        Calculate the line obtained by regressing points in bps_list.
        :param name: identifier for the resulting line
        :param bps: the bodyparts to use for the line
        :return: None
        """

        self.duplicate_name_check(name)
        m_arr = np.empty((self.nframes, 2))
        frames_w_invalid_reg = []
        bp_points = [self.bps[bp] for bp in bps]
        for frame in tqdm(range(self.start_frame, self.end_frame)):
            m = utils.regress(bp_points, frame)
            if m is None:
                frames_w_invalid_reg.append(frame)
                m_arr[frame] = [np.nan, np.nan]
            else:
                m_arr[frame] = m
        self.datastore[name] = m_arr

        if len(frames_w_invalid_reg) > 0:
            print("Not enough points to regress on frames", str(frames_w_invalid_reg), "for", name)
        print("Successfully regressed line for points", bps)

    def calc_perpendicular_line(self, name, line_name):
        """
        Calculate the line perpendicular to another line.
        Parameters:
            name (str): identifier for the resulting line
            line_name (str): identifier for the input line

        Returns:
            Nothing; adds the line identified by name to self.datastore
        """
        self.duplicate_name_check(name)
        m_arr = np.empty((self.nframes, 2))
        m_old_arr = self.datastore[line_name]

        print("\nStarting calculating line", name, "which is perpendicular to", line_name)
        for frame in tqdm(range(self.start_frame, self.end_frame)):
            m = (-1 / m_old_arr[frame][0], m_old_arr[frame][1])
            m_arr[frame] = m
        self.datastore[name] = m_arr
        print("Successfully calculated line", name, "which is perpendicular to", line_name)

    def calc_angle(self, name, line1_name, line2_name, fill_gaps=False):
        """
        Calculate the angle between two lines, where the angle from the
        first line to the second line is positive when clockwise and
        negative when counterclocksize.
        Parameters:
            name (str): identifier for the resulting angle
            line1_name (str): identifier for the first line
            line2_name (str): identifier for the second line
            fill_gaps (bool): when set to True, intopolate gaps to fill in
                              NaN values

        Returns:
            Nothing; adds the angle identified by name to self.datastore
        """
        self.duplicate_name_check(name)
        angle_arr = np.empty(self.nframes)
        m1_arr = self.datastore[line1_name]
        m2_arr = self.datastore[line2_name]

        print("\nStarting calculating angle", name, "between lines", line1_name, "and", line2_name)
        for frame in tqdm(range(self.start_frame, self.end_frame)):
            if m1_arr[frame] is [np.nan, np.nan] or m2_arr[frame] is [np.nan, np.nan]:
                angle_arr[frame] = np.nan
            else:
                m1 = m1_arr[frame][0]
                m2 = m2_arr[frame][0]
                angle_arr[frame] = utils.angle_between_lines(m1, m2)
        if fill_gaps:
            angle_arr = utils.math_utils.interpolate_gaps(angle_arr)
        self.datastore[name] = angle_arr
        print("Successfully calculated angle", name, "between lines", line1_name, "and", line2_name)

    def calc_avg(self, name: str, data_name_arr):
        """
        Calculate the vectorized average of several pieces of data.
        Parameters:
            name: str
                identifier for the resulting data
            data_name_arr: list of identifiers for the input
                                      data

        Returns:
            Nothing; adds the data identified by name to self.datastore
        """
        print("\nStarting calculating", name, "which is the average of", str(data_name_arr))
        data_stack = []
        for data_name in data_name_arr:
            data_stack.append(self.datastore[data_name])
        data_stack = np.vstack(tuple(data_stack))

        self.datastore[name] = np.average(data_stack, axis=0)
        print("Successfully calculated", name, "which is the average of", str(data_name_arr))

    def plot(self, y_name, label):
        x = range(self.start_frame, self.end_frame)
        y = self.datastore[y_name][self.start_frame : self.end_frame]
        plt.plot(x, y, label=label)

    def save_plot(self, xlabel, ylabel):
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

        outfile = self.outpath + xlabel + "_vs_" + ylabel
        plt.savefig(outfile, dpi=300)
        print(outfile, "saved!")

    def save_csv(self, col_names, filename):
        cols = []
        for name in col_names:
            cols.append(self.datastore[name].reshape(-1, 1))

        df = pandas.DataFrame(np.hstack(tuple(cols)))
        df.columns = col_names

        df.to_csv(os.path.join(self.outpath, filename))

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
