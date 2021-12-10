from dlc_generic_analysis.trimmer import GoToTime
from qtpy import QtWidgets


def test_go_to_time(qtbot):
    gtt = GoToTime()
    w = QtWidgets.QWidget()
    w.setLayout(gtt)
    qtbot.addWidget(w)


#  testing trimmer is too expensive
