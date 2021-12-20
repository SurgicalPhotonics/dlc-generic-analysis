from dlc_generic_analysis.viewer import ViewerWidget
import numpy as np


class VW(ViewerWidget):
    def __init__(self):
        super(VW, self).__init__()

    def position_changed(self, position):
        super(VW, self)._position_changed(position)

    def duration_changed(self, length):
        super(VW, self)._duration_changed(length)

    def on_load_video(self):
        super(VW, self).on_load_video()

    def load_video(self, path):
        super(VW, self)._load_video(path)

    def pause(self):
        super(VW, self).pause()

    def play(self):
        super(VW, self).play()


def test_viewer(qtbot):
    window = VW()
    # plots = FigureCanvas()
    # gs = plots.fig.add_gridspec(2, 1)
    # ax = [plots.fig.add_subplot(gs[0, 0]), plots.fig.add_subplot(gs[1, 0])]
    # data = np.linspace(0, 10, num=100)
    # data = np.sin(data)
    # data1 = np.linspace(0, 10, num=100)
    # data1 = np.cos(data1)
    # data1 = np.tan(data1)
    # data1 = np.diff(data1)
    # ax[0].plot(data)
    # ax[1].plot(data1)
    # window.content_layout.addWidget(plots)
    window.load_video("")
    # window.setBaseSize(window.sizeHint().width(), window.sizeHint().height())
    qtbot.addWidget(window)
    window.show()
