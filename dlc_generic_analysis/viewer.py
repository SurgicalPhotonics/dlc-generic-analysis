from qtpy import QtWidgets


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
        top_widget = QtWidgets.QWidget()
        top_widget.setLayout(QtWidgets.QHBoxLayout())
        top_widget.layout().addWidget(self.load_file_button)
        top_widget.layout().addWidget(self.matlab_button)
        top_widget.layout().addWidget(self.convert_button)
        self.top_widget = top_widget

        self.fast_reverse_button = QtWidgets.QPushButton("ff")
        self.play_pause_button = QtWidgets.QPushButton("p/p")
        self.fast_forward_button = QtWidgets.QPushButton("fr")
        self.goto_button = QtWidgets.QPushButton("Go To")
        self.seek_edit = QtWidgets.QLineEdit()
        self.scrub_bar = QtWidgets.QSlider()
        navigate_widget = QtWidgets.QWidget()
        navigate_widget.setLayout(QtWidgets.QGridLayout())
        navigate_widget.layout().addWidget(self.fast_reverse_button)
        navigate_widget.layout().addWidget(self.play_pause_button)
        navigate_widget.layout().addWidget(self.fast_forward_button)
        navigate_widget.layout().addWidget(self.goto_button)
        navigate_widget.layout().addWidget(self.seek_edit)
        navigate_widget.layout().addWidget(self.scrub_bar)
        self.navigate_widget = navigate_widget
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().addWidget(self.top_widget, 0, 0)


