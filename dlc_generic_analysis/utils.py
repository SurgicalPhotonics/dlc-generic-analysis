from typing import Tuple, List
import numpy as np
from pandas import DataFrame
import cv2

def dist(point1: Tuple[float, float], point2: Tuple[float, float]):
    return np.sqrt(
        np.abs(point2[0] - point1[0]) ** 2 + np.abs(point2[1] - point1[1]) ** 2
    )


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
