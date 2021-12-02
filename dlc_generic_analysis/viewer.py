import logging
import sys
from logging import info  # , error, warning
import numpy as np
from qtpy import QtWidgets, QtCore, QtMultimedia, QtMultimediaWidgets
from qtpy.QtCore import Qt
from gui_objects import PlayPause
import gui_utils
raster_plots = True
try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    # from matplotlib.backends.backend_qtcairo import FigureCanvasQTCairo as FigureCanvas
except OSError:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    logging.warning("Cairo could not be imported. using raster AGG plots")
from matplotlib.figure import Figure


class ViewWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ViewWidget, self).__init__()
        self.txt = QtWidgets.QLabel("Frame #")
        self.last_frame = -1
        self.playing = False
        self.loaded = False
        self.load_file_button = QtWidgets.QPushButton("Load File")
        self.matlab_button = QtWidgets.QPushButton("Export to MATLAB")
        self.convert_button = QtWidgets.QPushButton("Convert to MM")
        top_layout = QtWidgets.QHBoxLayout()
        # top_layout.setContentsMargins(10, 0, 10, 0)
        top_layout.addWidget(self.load_file_button)
        top_layout.addWidget(self.matlab_button)
        top_layout.addWidget(self.convert_button)
        self.top_layout = top_layout
        self.play_pause = PlayPause()
        self.play_pause.play_pause_button.clicked.connect(self.on_play_pause)
        self.play_pause.fast_forward_button.clicked.connect(self.on_fast_forward)
        self.play_pause.fast_reverse_button.clicked.connect(self.on_fast_reverse)
        self.goto_button = QtWidgets.QPushButton("Go To")
        self.seek_edit = QtWidgets.QLineEdit()
        self.scrub_bar = QtWidgets.QSlider(orientation=Qt.Horizontal)
        self.scrub_bar.sliderMoved.connect(self.on_slider_move)
        navigate_layout = QtWidgets.QGridLayout()
        navigate_layout.addLayout(self.play_pause,  0, 0)
        navigate_layout.addWidget(self.scrub_bar)
        self.content_layout = QtWidgets.QHBoxLayout()
        self.video_player = QtMultimedia.QMediaPlayer()
        self.video_player.setMuted(True)
        self.video_player.setNotifyInterval(5)
        self.video_player.positionChanged.connect(self.position_changed)
        self.video_player.stateChanged.connect(self.state_changed)
        self.video_player.durationChanged.connect(self.duration_changed)
        self.video_viewer = QtMultimediaWidgets.QVideoWidget()
        self.content_layout.addWidget(self.video_viewer)
        self.video_player.setVideoOutput(self.video_viewer)
        self.navigate_layout = navigate_layout
        self.setLayout(QtWidgets.QGridLayout())
        # self.layout().setContentsMargins(0, 0, 0, 0)
        # self.layout().setMargin(10)
        self.layout().addLayout(self.top_layout, 0, 0)
        self.layout().addLayout(self.content_layout, 1, 0)
        self.layout().addLayout(self.navigate_layout, 2, 0)
        self.load_video(sys.argv[1])

    def state_changed(self):
        if self.video_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            info("pause_icon")
            self.play_pause.play_pause_button.setIcon(self.play_pause.pause_icon)
        else:
            info("play icon")
            self.play_pause.play_pause_button.setIcon(self.play_pause.play_icon)

    def position_changed(self, position):
        self.scrub_bar.setValue(position)

    def duration_changed(self, length):
        self.scrub_bar.setRange(0, length)

    def on_play_pause(self):
        info(f"state = {self.video_player.state()}")
        if self.video_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.video_player.pause()
            info("pause")
        else:
            self.video_player.play()
            info("play")

    def on_fast_forward(self):
        if self.video_player.state() != QtMultimedia.QMediaPlayer.StoppedState:
            self.video_player.setPosition(self.video_player.position() + 1000)

    def on_fast_reverse(self):
        if self.video_player.state() != QtMultimedia.QMediaPlayer.StoppedState:
            self.video_player.setPosition(self.video_player.position() - 1000)

    def on_slider_move(self, position):
        self.video_player.setPosition(position)

    def on_load_video(self):
        video = gui_utils.open_files(self, "Select File to View")
        logging.info("Loading " + video)
        self.load_video(video)

    def load_video(self, path):
        self.video_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(path)))
        self.setMinimumWidth(int(self.width()/2))


class MplCanvasWidget(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication()
    window = ViewWidget()
    plots = MplCanvasWidget()
    ax = plots.fig.add_subplot()
    data = np.linspace(0, 100, num=50)
    ax.plot(data)
    window.content_layout.addWidget(plots)
    window.load_video(sys.argv[1])
    window.setBaseSize(window.sizeHint().width(), window.sizeHint().height())
    window.show()
    app.exec_()

