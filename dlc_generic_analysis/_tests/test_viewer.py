from dlc_generic_analysis.viewer import ViewWidget, MplCanvasWidget
import numpy as np


def test_viewer(qtbot):
    window = ViewWidget()
    plots = MplCanvasWidget()
    gs = plots.fig.add_gridspec(2, 1)
    ax = [plots.fig.add_subplot(gs[0, 0]), plots.fig.add_subplot(gs[1, 0])]
    data = np.linspace(0, 10, num=100)
    data = np.sin(data)
    data1 = np.linspace(0, 10, num=100)
    data1 = np.cos(data1)
    data1 = np.tan(data1)
    data1 = np.diff(data1)
    ax[0].plot(data)
    ax[1].plot(data1)
    window.content_layout.addWidget(plots)
    window.load_video("")
    window.setBaseSize(window.sizeHint().width(), window.sizeHint().height())
    qtbot.addWidget(window)
    window.show()
