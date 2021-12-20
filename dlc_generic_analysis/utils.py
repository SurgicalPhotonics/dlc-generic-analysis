import os.path
from typing import Tuple, List
import numpy as np
import scipy.spatial.distance
from pandas import DataFrame
import cv2
import urllib.request
import tarfile
from scipy import spatial
from scipy.spatial.distance import euclidean as dist


def distance(bp1, bp2, frame):
    p1 = (bp1["x"][frame], bp1["y"][frame])
    p2 = (bp2["x"][frame], bp2["y"][frame])

    d = spatial.distance.euclidean(p1, p2)
    return d


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


def down_sample(path, height=480):
    """
    down samples videos to be height tall
    :param path: the path to the source video
    :param height: the height of the downsampled video
    :return:
    """
    """Down samples high res videos to more manageable resolution for DeepLabCut"""
    cap = cv2.VideoCapture(path)
    src_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if src_height <= height:
        return path
    else:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frames = cap.get(cv2.CAP_PROP_FPS)
        r_height = 360
        ar = width / src_height
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


def angle_between_lines(m1: float, m2: float):
    """
    calculates the angle between 2 lines in degrees
    :param m1: slope of line 1
    :param m2: slope of line 2
    :return:
    """
    return np.degrees(np.arctan(((m2 - m1) / (1 + m1 * m2))))


def download_model(url: str, dest: str) -> str:
    """
    downloads a tarball model from url to dest/temp extracts it to dest/tar_name and returns the path of the
    model directory
    :param url: the url to download the model from
    :param dest: the destination to put the model
    :return: the path of the model directory
    """
    temp = os.path.join(dest, "temp")
    if not os.path.isdir(temp):
        os.mkdir(temp)
    model_tar = urllib.request.urlretrieve(url, temp)[0]
    if tarfile.is_tarfile(model_tar):
        ext = os.path.splitext(model_tar)[1]
        if ext == "gz" or ext == ".gz":
            tar = tarfile.open(model_tar, "r:gz")
        elif ext == "xz" or ext == ".xz":
            tar = tarfile.open(model_tar, "r:gz")
        else:
            raise ValueError("File must be .tar.gz or tar.xz")
    else:
        raise ValueError("File must be .tar.gz or tar.xz")
    name = os.path.splitext(os.path.split(model_tar)[1])[0]
    if not os.path.isdir(name):
        os.mkdir(name)
    tar.extractall(name)
    return name
