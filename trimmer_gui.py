import platform
import sys
from PySide2 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
from typing import List
from video_tools import Trimmer

class GoToTime(QtWidgets.QWidget):
    def __init__(self, text: str, time=0):
        super(GoToTime, self).__init__()
        self.text = text
        self.setLayout(QtWidgets.QHBoxLayout())
        self.label = QtWidgets.QLabel(f"{text} {round(time, 2)}")
        self.layout().addWidget(self.label)
        self.goto_button = QtWidgets.QPushButton("Go To")
        self.layout().addWidget(self.goto_button)

    def update_label(self, time):
        self.label = QtWidgets.QLabel(f"{self.text} {round(time, 2)}")


class TrimWidget(QtWidgets.QWidget):
    keyPressed = QtCore.Signal(int)

    def __init__(self, video_paths: List[str], parent=None):
        super(TrimWidget, self).__init__()
        self.setWindowTitle("Trim Video(s)")
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
        if len(video_paths) > 1:
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
        self.top_ui.filename_label = QtWidgets.QLabel("")

        self.video_viewer = QtMultimediaWidgets.QVideoWidget()
        self.video_viewer.resize(QtCore.QSize(1920, 1080))
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMuted(True)

        self.trim_beginning = 0  # the beginning point for the trim in milliseconds
        self.trim_end = self.player.duration()  # the end point for the trim in milliseconds
        self.play_pause_widget = QtWidgets.QWidget()
        self.play_pause_widget.setLayout(QtWidgets.QHBoxLayout())
        self.fast_reverse_button = QtWidgets.QPushButton()
        self.fast_reverse_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekForward))
        self.fast_reverse_button.clicked.connect(self.on_click_fast_reverse)
        self.play_pause_widget.layout().addWidget(self.fast_reverse_button)
        self.play_pause_button = QtWidgets.QPushButton()
        self.play_pause_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.play_pause_button.clicked.connect(self.on_click_play_pause)
        self.play_pause_widget.layout().addWidget(self.play_pause_button)
        self.fast_forward_button = QtWidgets.QPushButton()
        self.fast_reverse_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekBackward))
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
        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.on_slider_move)
        self.goto_start = GoToTime("Start Time")
        self.goto_end = GoToTime("End Time")
        self.subclip_duration_label = QtWidgets.QLabel(f"Sub-clip Duration {self.subclip_duration}")
        self.finish_buttom = QtWidgets.QPushButton("Finish")
        self.finish_buttom.clicked.connect(self.on_click_finish)
        self.trim_control = QtWidgets.QWidget()
        self.trim_control.setLayout(QtWidgets.QGridLayout())
        x, y = 0, 0
        self.trim_control.layout().addWidget(self.play_pause_widget, x, y)
        y += 1
        self.trim_control.layout().addWidget(self.trim_buttons_widget, x, y)
        y = 0
        x += 1
        self.trim_control.layout().addWidget(self.slider, x, y, x, y+2)
        x += 1
        self.trim_control.layout().addWidget(self.goto_start, x, y)
        y += 1
        self.trim_control.layout().addWidget(self.goto_end, x, y)
        y= 0
        x +=1
        self.trim_control.layout().addWidget(self.subclip_duration_label, x, y)
        y += 1
        self.trim_control.layout().addWidget(self.finish_buttom, x, y)
        self.layout().addWidget(self.top_ui)
        self.layout().addWidget(self.video_viewer, alignment=QtCore.Qt.AlignCenter)
        self.layout().addWidget(self.trim_control)
        self.player.stateChanged.connect(self.state_changed)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.setVideoOutput(self.video_viewer)
        self.load_video(self.video_paths[0])

    def load_video(self, path):
        self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(path)))

    def on_click_play_pause(self, e):
        state = self.player.state()
        print(f"state = {state}")
        if state == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.pause()
            print("pause")
        else:
            self.player.play()
            print("play")

    def on_click_fast_forward(self, e):
        if self.player.state() != QtMultimedia.QMediaPlayer.StoppedState:
            self.player.setPosition(self.player.position()+1000)

    def on_click_fast_reverse(self, e):
        if self.player.state() != QtMultimedia.QMediaPlayer.StoppedState:
            self.player.setPosition(self.player.position()-1000)

    def on_slider_move(self, position):
        self.player.setPosition(position)

    def on_click_trim_start(self, e):
        self.trim_beginning = self.player.position()
        if self.trim_end < self.trim_beginning:
            self.trim_end = self.trim_beginning
        self.goto_start.update_label(self.trim_beginning)
        subclip_duration = (self.trim_end - self.trim_beginning) / 1000
        self.subclip_duration_label.setText(f"Sub-clip Duration {subclip_duration}")

    def on_click_trim_end(self, e):
        self.trim_end = self.player.position()
        self.goto_end.update_label(self.trim_end)
        subclip_duration = (self.trim_end - self.trim_beginning) / 1000
        self.subclip_duration_label.setText(f"Sub-clip Duration {subclip_duration}")
        if self.trim_beginning> self.trim_end:
            self.trim_beginning = self.trim_end

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

    def state_changed(self, e):
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.play_pause_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.play_pause_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, length):
        self.slider.setRange(0, length)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super(TrimWidget, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def on_keypress(self, key):
        if key == QtCore.Qt.Key_space:
            if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
                self.player.pause()
            else:
                self.player.play()
        if key == QtCore.Qt.Key_Forward:
            pass

    def on_click_finish(self, e):
        pass


if __name__ == '__main__':
    videos = [sys.argv[1]]
    print("video " + videos[0])
    app = QtWidgets.QApplication()
    window = TrimWidget(videos)
    window.resize(640, 640)
    window.show()
    app.exec_()

