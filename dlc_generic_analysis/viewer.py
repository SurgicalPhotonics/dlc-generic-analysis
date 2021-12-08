from logging import info  # , error, warning
from abc import abstractmethod, ABCMeta
from qtpy import QtWidgets, QtCore, QtMultimedia, QtMultimediaWidgets
from qtpy.QtCore import Qt
from .gui_objects import PlayPause
from . import gui_utils

try:
    from matplotlib.backends.backend_qtcairo import FigureCanvasQTCairo as FigureCanvasQT
except (OSError, ImportError) as e:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvasQT

    info("Cairo could not be imported. using raster AGG plots " + str(e))
from matplotlib.figure import Figure


class ViewWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ViewWidget, self).__init__()
        self.txt = QtWidgets.QLabel("Frame #")
        self.frame_rate = 1
        self.last_frame = -1
        self.playing = False
        self.loaded = False
        self._load_file_button = QtWidgets.QPushButton("Load File")
        self._matlab_button = QtWidgets.QPushButton("Export to MATLAB")
        self._convert_button = QtWidgets.QPushButton("Convert to MM")
        self._top_layout = QtWidgets.QHBoxLayout()
        self._top_layout.addWidget(self._load_file_button)
        self._top_layout.addWidget(self._matlab_button)
        self._top_layout.addWidget(self._convert_button)
        self._play_pause = PlayPause()
        self._play_pause.play_pause_button.clicked.connect(self.on_play_pause)
        self._play_pause.fast_forward_button.clicked.connect(self.on_fast_forward)
        self._play_pause.fast_reverse_button.clicked.connect(self.on_fast_reverse)
        self._goto_button = QtWidgets.QPushButton("Go To")
        self._seek_edit = QtWidgets.QLineEdit()
        self._scrub_bar = QtWidgets.QSlider(orientation=Qt.Horizontal)
        self._scrub_bar.sliderMoved.connect(self.on_slider_move)
        self._navigate_layout = QtWidgets.QGridLayout()
        self._navigate_layout.addLayout(self._play_pause, 0, 0)
        self._navigate_layout.addWidget(self._scrub_bar)
        self.content_layout = QtWidgets.QHBoxLayout()
        self._video_player = QtMultimedia.QMediaPlayer()
        self._video_player.setMuted(True)
        self._video_player.setNotifyInterval(5)
        self._video_player.positionChanged.connect(self.position_changed)
        self._video_player.stateChanged.connect(self.state_changed)
        self._video_player.durationChanged.connect(self.duration_changed)
        self.video_viewer = QtMultimediaWidgets.QVideoWidget()
        self.content_layout.addWidget(self.video_viewer)
        self._video_player.setVideoOutput(self.video_viewer)
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().addLayout(self._top_layout, 0, 0)
        self.layout().addLayout(self.content_layout, 1, 0)
        self.layout().addLayout(self._navigate_layout, 2, 0)

    def state_changed(self):
        if self._video_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            info("pause_icon")
            self._play_pause.play_pause_button.setIcon(self._play_pause.pause_icon)
        else:
            info("play icon")
            self._play_pause.play_pause_button.setIcon(self._play_pause.play_icon)

    @abstractmethod
    def position_changed(self, position):
        self._scrub_bar.setValue(position)

    @abstractmethod
    def duration_changed(self, length):
        self._scrub_bar.setRange(0, length)

    def on_play_pause(self):
        info(f"state = {self._video_player.state()}")
        if self._video_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.pause()
            info("pause")
        else:
            self.play()
            info("play")

    def on_fast_forward(self):
        if self._video_player.state() != QtMultimedia.QMediaPlayer.StoppedState:
            self._video_player.setPosition(self._video_player.position() + 1000)

    def on_fast_reverse(self):
        if self._video_player.state() != QtMultimedia.QMediaPlayer.StoppedState:
            self._video_player.setPosition(self._video_player.position() - 1000)

    def on_slider_move(self, position):
        self._video_player.setPosition(position)

    @abstractmethod
    def on_load_video(self):
        video = gui_utils.open_files(self, "Select File to View")
        info("Loading " + video)
        self.load_video(video)

    @abstractmethod
    def load_video(self, path):
        self._video_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(path)))
        self.setMinimumWidth(int(self.width() / 2))

    @abstractmethod
    def pause(self):
        self._video_player.pause()

    @abstractmethod
    def play(self):
        self._video_player.play()

    def ms_to_frame(self, ms):
        return ms / 1000 * self.frame_rate

    def frame_to_ms(self, frame):
        return frame / self.frame_rate * 1000


class MplCanvasWidget(FigureCanvasQT):
    def __init__(self):
        self.fig = Figure()
        FigureCanvasQT.__init__(self, self.fig)
