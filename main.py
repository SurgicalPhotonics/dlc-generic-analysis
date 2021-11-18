from PySide2 import QtWidgets, QtCore, QtGui
# from qtpy import QtWidgets, QtCore, QtGui
from abc import ABC


class MainWidget(QtWidgets.QWidget, ABC):

    def __init__(self, model_path):
        super(MainWidget, self).__init__()
        self.setLayout(QtWidgets.QGridLayout())
        self.dlc_model_path = model_path
        self.crop_checkbox = QtWidgets.QCheckBox("Crop Videos")
        self.layout().addWidget(self.crop_checkbox)
        self.analyze_button = QtWidgets.QPushButton("Analyze Videos")
        self.layout().addWidget(self.analyze_button)
        self.view_button = QtWidgets.QPushButton("View Analyzed Video")
        self.layout().addWidget(self.view_button)
        self.trim_button = QtWidgets.QPushButton("Trim Videos")
        self.layout().addWidget(self.trim_button)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
