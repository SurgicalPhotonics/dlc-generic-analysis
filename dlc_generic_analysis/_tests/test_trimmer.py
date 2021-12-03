from dlc_generic_analysis.trimmer import Trimmer


def test_trimmer(qtbot):
    trimmer = Trimmer([""])
    trimmer.show()
    qtbot.addWidget(trimmer)
