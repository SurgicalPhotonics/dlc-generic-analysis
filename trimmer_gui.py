import platform
import sys

from PySide2 import QtWidgets, QtCore, QtMultimedia, QtMultimediaWidgets
from typing import List


class GoToTime(QtWidgets.QWidget):
    def __init__(self, text: str, time=0):
        super(GoToTime, self).__init__()
        self.time = time
        self.setLayout(QtWidgets.QHBoxLayout())
        self.label = QtWidgets.QLabel(f"{text} {round(self.time, 2)}")
        self.layout().addWidget(self.label)
        self.goto_button = QtWidgets.QPushButton("Go To")
        self.layout().addWidget(self.goto_button)


class TrimWidget(QtWidgets.QWidget):
    def __init__(self, video_paths: List[str], parent=None):
        super(TrimWidget, self).__init__()
        if platform.system() == "Windows":
            fast_reverse = "\u23EA"
            fast_forward = "\u23E9"
            play_pause = "\u23EF"
        else:
            fast_reverse = "\u23ea"
            fast_forward = "\u23e9"
            play_pause = "\u23ef"
        self.setLayout(QtWidgets.QGridLayout())
        self.video_loaded = False
        self.video_playing = False
        self.video_paths = video_paths
        self.current_video_index = 0
        self.subclip_duration = 0
        self.setParent(parent)
        self.top_ui = QtWidgets.QWidget()
        self.top_ui.setLayout(QtWidgets.QHBoxLayout())
        self.top_ui.videos_navigate = QtWidgets.QWidget()
        self.videos_navigate = QtWidgets.QWidget()
        self.videos_navigate.setLayout(QtWidgets.QHBoxLayout())
        self.previous_video_button = QtWidgets.QPushButton("Previous Video")
        self.previous_video_button.clicked.connect(self.on_click_previous_video)
        self.previous_video_button.setDisabled(True)
        self.videos_navigate.layout().addWidget(self.previous_video_button)
        self.next_video_button = QtWidgets.QPushButton("Next Video")
        self.next_video_button.clicked.connect(self.on_click_next_video)
        self.videos_navigate.layout().addWidget(self.next_video_button)
        self.top_ui.layout().addWidget(self.videos_navigate)
        self.top_ui.filename_label = QtWidgets.QLabel(self.video_paths[0])

        self.video_viewer = QtMultimediaWidgets.QVideoWidget()
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVideoOutput(self.video_viewer)
        self.player.setMuted(True)

        self.load_video(self.video_paths[0])
        self.trim_beginning = 0  # the beginning point for the trim in milliseconds
        self.trim_end = self.player.duration()  # the end point for the trim in milliseconds
        self.play_pause_widget = QtWidgets.QWidget()
        self.play_pause_widget.setLayout(QtWidgets.QHBoxLayout())
        self.fast_reverse_button = QtWidgets.QPushButton(fast_reverse)
        self.fast_reverse_button.clicked.connect(self.on_click_fast_reverse)
        self.play_pause_widget.layout().addWidget(self.fast_reverse_button)
        self.play_pause_button = QtWidgets.QPushButton(play_pause)
        self.play_pause_button.clicked.connect(self.on_click_play_pause)
        self.play_pause_widget.layout().addWidget(self.play_pause_button)
        self.fast_forward_button = QtWidgets.QPushButton(fast_forward)
        self.fast_forward_button.clicked.connect(self.on_click_fast_forward)
        self.play_pause_widget.layout().addWidget(self.fast_forward_button)

        self.trim_buttons_widget = QtWidgets.QWidget()
        self.trim_buttons_widget.setLayout(QtWidgets.QHBoxLayout())
        self.trim_start_button = QtWidgets.QPushButton("Trim Start")
        self.trim_start_button.clicked.connect(self.on_click_trim_start)
        self.trim_buttons_widget.layout().addWidget(self.trim_start_button)
        self.trim_end_button = QtWidgets.QPushButton("Trim End")
        self.trim_end_button.clicked.connect(self.on_click_trim_end)
        self.trim_buttons_widget.layout().addWidget(self.trim_end_button)
        self.goto_start = GoToTime("Start Time")
        self.goto_end = GoToTime("End Time")
        self.subclip_duration_label = QtWidgets.QLabel(f"Sub-clip Duration {self.subclip_duration}")
        self.trim_control = QtWidgets.QWidget()
        self.trim_control.setLayout(QtWidgets.QGridLayout())
        self.trim_control.layout().addWidget(self.play_pause_widget)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.trim_control.layout().addWidget(self.slider)
        self.trim_control.layout().addWidget(self.trim_buttons_widget)
        self.trim_control.layout().addWidget(self.goto_start)
        self.trim_control.layout().addWidget(self.goto_end)
        self.trim_control.layout().addWidget(self.subclip_duration_label)
        self.layout().addWidget(self.top_ui)
        self.layout().addWidget(self.video_viewer)
        self.layout().addWidget(self.trim_control)
        # self.loop = QtCore.QEventLoop(self)
        # self.loop.processEvents(self.e)
        self.show()
        # self.loop.exec_()

    def load_video(self, path):
        self.player.setMedia(QtCore.QUrl.fromLocalFile(path))

    def on_click_play_pause(self, e):
        state = self.player.state()
        if state == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.pause()
        elif state == QtMultimedia.QMediaPlayer.PausedState:
            self.player.play()
        elif state == QtMultimedia.QMediaPlayer.StoppedState:
            pass
            # play from beginning

    def on_click_fast_forward(self, e):
        if self.player.playbackState() != QtMultimedia.QMediaPlayer.StoppedState:
            self.player.setPosition(self.player.position()+1000)

    def on_click_fast_reverse(self, e):
        if self.player.playbackState() != QtMultimedia.QMediaPlayer.StoppedState:
            self.player.setPosition(self.player.position()-1000)

    def on_click_trim_start(self, e):
        self.trim_beginning = self.player.position()

    def on_click_trim_end(self, e):
        self.trim_end = self.player.position()

    def on_click_previous_video(self, e):
        if self.current_video_index > 0:
            self.current_video_index -= 1
            self.load_video(self.video_paths[self.current_video_index])
            if self.current_video_index == 0:
                self.previous_video_button.setEnabled(False)
            if self.current_video_index < len(self.video_paths)-1:
                self.next_video_button.setEnabled(True)

    def on_click_next_video(self, e):
        if self.current_video_index < len(self.video_paths)-1:
            self.current_video_index += 1
            if self.current_video_index > 0:
                self.previous_video_button.setEnabled(True)
            if self.current_video_index == len(self.video_paths)-1:
                self.next_video_button.setEnabled(False)
            self.load_video(self.video_paths[self.current_video_index])

    def on_close(self, e):
        self.loop.quit()
        self.destroy()


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = TrimWidget(sys.argv[1:])
    app.exec_()

