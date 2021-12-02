import multiprocessing
import os
import sys
from PySide6 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
from gui_objects import PlayPause
from typing import List, Tuple
from moviepy.editor import VideoFileClip


def trim_pool(args: Tuple[str, float, float]) -> None:
    """
    trims a file and writes it to a new file with "_trimmed" appended to the end
    :param args: A tuple of (str, float, float) where str is the video path, the first float is the
    start of the trim region and the second float is the end of the trim region
    :return: None
    """
    clip = VideoFileClip(args[0])
    clip.cutout(args[1] / 1000, args[2] / 1000)
    fname, ext = os.path.splitext(args[0])
    outfile = fname + "_trimmed" + ext
    clip.write_videofile(outfile)


class GoToTime(QtWidgets.QHBoxLayout):
    def __init__(self, text: str = "", time: float = 0):
        """
        A button that says go to with an editable label
        :param text: the text of the label
        :param time: the initial time value
        """
        super(GoToTime, self).__init__()
        self.text = text
        self.setContentsMargins(0, 0, 0, 0)
        self.setMargin(0)
        if text != "":
            self.label = QtWidgets.QLabel(f"{text} {round(time, 2)}")
        # self.label.setFixedWidth(100)
        self.addWidget(self.label)
        self.goto_button = QtWidgets.QPushButton("Go To")
        self.addWidget(self.goto_button)

    def update_label(self, time):
        self.label.setText(f"{self.text} {round(time, 2)}")


class Trimmer(QtWidgets.QWidget):
    keyPressed = QtCore.Signal(int)

    def __init__(self, video_paths: List[str]):
        super(Trimmer, self).__init__()
        self.setWindowTitle("Trim Video(s)")
        self.setLayout(QtWidgets.QVBoxLayout())
        self.video_loaded = False
        self.video_playing = False
        self.video_paths = video_paths
        self.current_video_index = 0
        self.top_ui = QtWidgets.QVBoxLayout()
        self.top_ui.setContentsMargins(0, 0, 0, 0)
        self.videos_navigate = QtWidgets.QHBoxLayout()
        self.previous_video_button = QtWidgets.QPushButton("Previous Video")
        self.previous_video_button.clicked.connect(self.on_click_previous_video)
        self.previous_video_button.setDisabled(True)
        self.videos_navigate.addWidget(self.previous_video_button)
        self.next_video_button = QtWidgets.QPushButton("Next Video")
        if len(self.video_paths) < 2:
            self.next_video_button.setDisabled(True)
        self.next_video_button.clicked.connect(self.on_click_next_video)
        self.videos_navigate.addWidget(self.next_video_button)
        self.filename_label = QtWidgets.QLabel(" ")
        self.filename_label.setMargin(0)
        self.videos_navigate.setContentsMargins(0, 0, 0, 0)
        self.top_ui.addLayout(self.videos_navigate)
        self.top_ui.setMargin(0)
        self.video_viewer = QtMultimediaWidgets.QVideoWidget()
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMuted(True)
        self.trim_start = [0] * len(
            self.video_paths
        )  # the beginning point for the trim in milliseconds
        self.trim_end = [0] * len(self.video_paths)  # the end point for the trim in milliseconds
        self.play_pause = PlayPause()
        self.play_pause.fast_reverse_button.clicked.connect(self.on_click_fast_reverse)
        self.play_pause.play_pause_button.clicked.connect(self.on_click_play_pause)
        self.play_pause.fast_forward_button.clicked.connect(self.on_click_fast_forward)
        self.trim_buttons = QtWidgets.QHBoxLayout()
        self.trim_buttons.setContentsMargins(0, 0, 0, 0)
        self.trim_start_button = QtWidgets.QPushButton("Trim Start")
        self.trim_start_button.clicked.connect(self.on_click_trim_start)
        self.trim_buttons.addWidget(self.trim_start_button)
        self.trim_end_button = QtWidgets.QPushButton("Trim End")
        self.trim_end_button.clicked.connect(self.on_click_trim_end)
        self.trim_buttons.addWidget(self.trim_end_button)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.on_slider_move)
        self.goto_start = GoToTime("Start Time")
        self.goto_start.goto_button.clicked.connect(self.on_goto_start)
        self.goto_end = GoToTime("End Time")
        self.goto_end.goto_button.clicked.connect(self.on_goto_end)
        self.subclip_duration_label = QtWidgets.QLabel(f"Sub-clip Duration {0}")
        self.finish_buttom = QtWidgets.QPushButton("Finish")
        self.finish_buttom.clicked.connect(self.on_click_finish)
        self.trim_control = QtWidgets.QGridLayout()
        self.trim_control.setContentsMargins(0, 0, 0, 0)
        print(f"veritcal spacing {self.trim_control.verticalSpacing()}")
        x, y = 0, 0
        self.trim_control.addLayout(self.play_pause, 0, 0)
        self.trim_control.addLayout(self.trim_buttons, 0, 2)
        y = 0
        x += 1
        self.trim_control.addWidget(self.slider, x, y, x, -1)
        y = 0
        x += 1
        self.trim_control.addLayout(self.goto_start, x, y)
        y += 1
        self.trim_control.addLayout(self.goto_end, x, y)
        y += 1
        self.trim_control.addWidget(self.subclip_duration_label, x, y)
        y += 1
        self.trim_control.addWidget(self.finish_buttom, x, y)
        print(
            f"num rows {self.trim_control.rowCount()} = num columns = {self.trim_control.columnCount()}"
        )
        # self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addLayout(self.top_ui, aligment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.layout().addWidget(self.video_viewer)
        self.layout().addLayout(self.trim_control)
        self.player.setVideoOutput(self.video_viewer)
        self.player.stateChanged.connect(self.state_changed)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.load_video(self.video_paths[self.current_video_index])

    def load_video(self, path):
        self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(path)))
        self.filename_label.setText(os.path.split(path)[1])
        self.filename_label.resize(self.filename_label.sizeHint())
        self.trim_end[self.current_video_index] = self.player.duration()
        subclip_duration = (
            self.trim_end[self.current_video_index] / 1000
            - self.trim_start[self.current_video_index] / 1000
        )
        self.subclip_duration_label.setText(f"Sub-clip Duration {subclip_duration}")

    def on_click_previous_video(self, e):
        if self.current_video_index > 0:
            self.current_video_index -= 1
            self.load_video(self.video_paths[self.current_video_index])
            if self.current_video_index == 0:
                self.previous_video_button.setEnabled(False)
            if self.current_video_index < len(self.video_paths) - 1:
                self.next_video_button.setEnabled(True)

    def on_click_next_video(self, e):
        if self.current_video_index < len(self.video_paths) - 1:
            self.current_video_index += 1
            if self.current_video_index > 0:
                self.previous_video_button.setEnabled(True)
            if self.current_video_index == len(self.video_paths) - 1:
                self.next_video_button.setEnabled(False)
            self.load_video(self.video_paths[self.current_video_index])

    def on_click_play_pause(self, e):
        print(f"state = {self.player.state()}")
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.pause()
            print("pause")
        else:
            self.player.play()
            print("play")

    def on_click_fast_forward(self, e):
        if self.player.state() != QtMultimedia.QMediaPlayer.StoppedState:
            self.player.setPosition(self.player.position() + 1000)

    def on_click_fast_reverse(self, e):
        if self.player.state() != QtMultimedia.QMediaPlayer.StoppedState:
            self.player.setPosition(self.player.position() - 1000)

    def on_slider_move(self, position):
        self.player.setPosition(position)

    def on_click_trim_start(self, e):
        print(f"current position {self.player.position()}")
        self.trim_start[self.current_video_index] = self.player.position()
        self.goto_start.update_label(self.trim_start[self.current_video_index] / 1000)

        if self.trim_end[self.current_video_index] < self.trim_start[self.current_video_index]:
            self.trim_end[self.current_video_index] = self.trim_start[self.current_video_index]
        subclip_duration = (
            self.trim_end[self.current_video_index] / 1000
            - self.trim_start[self.current_video_index] / 1000
        )
        self.subclip_duration_label.setText(f"Sub-clip Duration {subclip_duration}")
        print(f"subclip_duration {subclip_duration}")

    def on_click_trim_end(self, e):
        self.trim_end[self.current_video_index] = self.player.position()
        print(f"current position {self.trim_end[self.current_video_index] }")

        self.goto_end.update_label(self.trim_end[self.current_video_index] / 1000)
        if self.trim_start > self.trim_end:
            self.trim_start = self.trim_end
        subclip_duration = (
            self.trim_end[self.current_video_index] / 1000
            - self.trim_start[self.current_video_index] / 1000
        )
        print(f"subclip_duration {subclip_duration}")
        self.subclip_duration_label.setText(f"Sub-clip Duration {subclip_duration}")

    def on_close(self, e):
        self.loop.quit()
        self.destroy()

    def state_changed(self, e):
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.play_pause_button.setIcon(self.pause_icon)
        else:
            self.play_pause_button.setIcon(self.play_icon)

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, length):
        self.slider.setRange(0, length)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super(Trimmer, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def on_goto_start(self, e):
        self.player.setPosition(self.trim_start[self.current_video_index])

    def on_goto_end(self, e):
        self.player.setPosition(self.trim_end[self.current_video_index])

    def on_click_finish(self, e):
        args = zip(self.video_paths, self.trim_start, self.trim_end)
        with multiprocessing.Pool() as pool:
            pool.imap_unordered(trim_pool, args)
        print("done")
        app.exit(0)


if __name__ == "__main__":
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    videos = sys.argv[1:]
    print("video " + videos[0])
    app = QtWidgets.QApplication()
    window = Trimmer(videos)
    window.resize(1280, 800)
    window.show()
    app.exec_()
