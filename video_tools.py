import os
import cv2
from typing import List
import moviepy.editor
from trimmer_gui import TrimWidget


def resize(path: str, width):
    clip = moviepy.editor.VideoFileClip(path)
    clip_resized = clip.resize(width=width)
    filename, extension = os.path.splitext(path)
    clip_resized.write_videofile(filename + "_resized" + extension)


class Trimmer:
    def __init__(self, videopaths: List[str], show: bool = False):
        """

        :param videopaths:
        :param show:
        """
        self.clips = []
        self.start = []
        self.end = []
        self.duration = []
        self.trimmed_clips = []
        self.videopaths = videopaths
        self.trimmed_paths = []
        self.finish = False
        # Add Error checking for good path!!!
        if videopaths is not None:
            for i, path in enumerate(videopaths):
                self.clips.append(moviepy.editor.VideoFileClip(path))
                self.init_clip(path, i)
        else:
            self.clips = None
            self.start = None
            self.end = None
            self.duration = None
            self.trimmed_clips = None

        self.frame = None

        if show:
            self.show()

    def setclips(self, videopaths):
        if videopaths is not None:
            for i, path in enumerate(videopaths):
                self.clips.append(moviepy.editor.VideoFileClip(path))
                self.init_clip(i, path)
        else:
            raise NotImplementedError

    def init_clip(self, path, i):
        self.start.insert(i, 0.0)
        self.end.insert(i, 0.0)
        self.duration.insert(i, 0.0)
        self.trimmed_clips.insert(i, self.clips[i])

        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)

        self.clips[i].set_fps(fps)

    def set_range(self, i, start, end):
        clip = self.clips[i]
        assert start >= clip.start and end <= clip.end

        self.end[i] = end
        self.start[i] = start

    def get_range(self, i):
        return self.start[i], self.end[i]

    def trim(self, i, start: float = 0, end: float = 0):
        """

        :param i: the index of the clip to trim
        :param start: the start of the trimmed portion in decimal seconds
        :param end: the end of the trimmed portion in decimal seconds
        :return: None
        """
        if start is not None and end is not None:
            self.trimmed_clips[i] = self.clips[i].cutout(start, end)
        else:
            start = self.start[i]
            end = self.end[i]
            if end > start:
                self.trimmed_clips[i] = self.clips[i].cutout(start, end)

    def get_paths(self):
        return self.videopaths

    # def show(self):
    #     self.frame = TrimFrame(self, self.videopaths)

    def write_to_file(self, i, outpath):
        self.trimmed_clips[i].write_videofile(outpath)
        self.trimmed_paths.insert(i, outpath)

    def get_trimmed_paths(self) -> List[str]:
        return self.trimmed_paths

    def close(self):
        self.frame.Close()
        self.frame.Destroy()
        self.finish = True

    def show(self):
        self.frame = TrimWidget(self, self.videopaths)
