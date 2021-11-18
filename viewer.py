from qtpy import QtWidgets, QtCore, QtGui
from qtpy import QtMultimedia


class ViewWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ViewWidget, self).__init__()
        self.txt = QtWidgets.QLabel("Frame #")
        self.last_frame = -1
        self.playing = False
        self.loaded = False


        self.load_file_button = QtWidgets.QPushButton("Load File")
        self.matlab_button = QtWidgets.QPushButton("Export to Matlab")
        self.convert_button = QtWidgets.QPushButton("Convert to MM")
        self.top_widget = QtWidgets.QWidget()
        self.top_widget.setLayout(QtWidgets.QHBoxLayout())
        self.top_widget.layout().addWidget(self.load_file_button)
        self.top_widget.layout().addWidget(self.matlab_button)
        self.top_widget.layout().addWidget(self.convert_button)

        self.fast_reverse_button = QtWidgets.QPushButton("ff")
        self.fast_forward_button = QtWidgets.QPushButton("fr")
        self.goto_button = QtWidgets.QPushButton("p/p")
        self.scub_bar = QtWidgets.QSlider

        self.convert_button = QtWidgets.QPushButton()

