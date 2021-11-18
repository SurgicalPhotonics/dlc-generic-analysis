import os.path
from deeplabcut import analyze_videos
from typing import List


def analyze(config: str, paths: List[str], gputouse: int = -1) -> (List[str], str):
    """
    DLC analyze videos or a batch of videos with the same file extension. will use the 0th paths extension for encoding
    :param config: the directory containing the config.yaml file
    :param paths: the paths to the videos to be analyzed
    :param gputouse: the CUDA capable Nvidia GPU to use for inference if not set GPU inference will be disabled
    :return h5, slug: h5: a list of the h5 paths from the analysis, slug: the name of then DLC model in the h5 file
    """
    cfg = os.path.join(config, "config.yaml")
    _, vidtype = os.path.splitext(paths[0])
    dest, _ = os.path.split(paths[0])
    if gputouse >= 0:
        slug = analyze_videos(
            cfg, paths, videotype=vidtype, destfolder=dest, gputouse=gputouse, save_as_csv=True
        )
    else:
        slug = analyze_videos(
            cfg, paths, videotype=vidtype, destfolder=dest, gputouse=None, save_as_csv=True, TFGPUinference=False
        )
    h5 = []
    for path in paths:
        h5.append(os.path.join(dest, os.path.splitext(os.path.split(path)[1])[0] + slug + ".h5"))
    return h5, slug