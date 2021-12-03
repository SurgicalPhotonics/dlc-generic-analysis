import csv
from typing import Tuple, List
import numpy as np
from pandas import DataFrame
import cv2


def dist(point1: Tuple[float, float], point2: Tuple[float, float]):
    return np.sqrt(np.abs(point2[0] - point1[0]) ** 2 + np.abs(point2[1] - point1[1]) ** 2)


def point_array(data_frame: DataFrame, points: List[str]):
    nd_arrays = list()
    for point in points:
        nd_arrays.append(data_frame[point].to_numpy(dtype=np.float64))
    return np.stack(nd_arrays, axis=0)[:, :, 0:2]


def to_avi(in_path, out_path):
    """can only play AVI in wx media player so mp4 must be converted."""
    video_cap = cv2.VideoCapture(in_path)
    fps = video_cap.get(cv2.CAP_PROP_FPS)
    size = (
        int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    fourcc = cv2.VideoWriter.fourcc("x", "v", "i", "d")
    video_writer = cv2.VideoWriter(out_path, fourcc, fps, size)

    success, frame = video_cap.read()
    while success:
        video_writer.write(frame)
        success, frame = video_cap.read()


def read_data(path: str):
    with open(path, "r") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)
        data = []
        for row in reader:
            data.append(float(row[7]))
    return data


def down_sample(path):
    """Down samples high res videos to more manageable resolution for DeepLabCut"""
    cap = cv2.VideoCapture(path)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if height <= 480:
        return path
    else:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frames = cap.get(cv2.CAP_PROP_FPS)
        r_height = 360
        ar = width / height
        r_width = int(ar * 360)
        fourcc = cv2.VideoWriter.fourcc("m", "p", "4", "v")
        name = path[: path.rfind(".")] + "_resized.mp4"
        writer = cv2.VideoWriter(name, fourcc, frames, (r_width, r_height))
        s, im = cap.read()
        while s:
            image = cv2.resize(im, (r_width, r_height))
            writer.write(image)
            s, im = cap.read()
        return name


def angle_between_lines(m1, m2):
    return np.degrees(np.arctan(((m2 - m1) / (1 + m1 * m2))))


#
# def plot_regres(m, b):
#     x = np.linspace(0, 1280, 100)
#     y = m * x + b
#     plt.plot(x, y, color="red")
