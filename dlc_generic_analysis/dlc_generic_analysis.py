from qtpy import QtWidgets
from qtpy.QtCore import Qt
from .trimmer import Trimmer
from abc import abstractmethod


class MainWidget(QtWidgets.QWidget):
    def __init__(self, model_path):
        super(MainWidget, self).__init__()
        self.setLayout(QtWidgets.QGridLayout())
        self.title = QtWidgets.QLabel("")
        self.layout().addWidget(self.title, alignment=Qt.AlignHCenter)
        self.dlc_model_path = model_path
        self.crop_checkbox = QtWidgets.QCheckBox("Crop Videos")
        self.layout().addWidget(self.crop_checkbox)
        self.analyze_button = QtWidgets.QPushButton("Analyze Videos")
        self.analyze_button.clicked.connect(self.on_click_analyze)
        self.layout().addWidget(self.analyze_button)
        self.view_button = QtWidgets.QPushButton("View Analyzed Video")
        self.view_button.clicked.connect(self.on_click_view)
        self.layout().addWidget(self.view_button)
        self.trim_button = QtWidgets.QPushButton("Trim Videos")
        self.trim_button.clicked.connect(self.on_click_trim)
        self.layout().addWidget(self.trim_button)

    @abstractmethod
    def on_click_analyze(self):
        pass

    @abstractmethod
    def on_click_view(self):
        pass

    @abstractmethod
    def on_click_trim(self):
        vids = self.open_files("Select videos to trim")
        trimmer = Trimmer(vids)
        trimmer.show()
