import sys

# from PySide2 import QtWidgets, QtCore, QtGui
from qtpy import QtWidgets, QtCore, QtGui
from abc import ABC, abstractmethod

import video_tools


class MainWidget(QtWidgets.QWidget):

    def __init__(self, model_path):
        super(MainWidget, self).__init__()
        self.setLayout(QtWidgets.QGridLayout())
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

    def on_click_analyze(self):
        pass

    def on_click_view(self):
        pass

    def on_click_trim(self):
        vids = self.open_files("Select videos to trim")
        trimmer = video_tools.Trimmer(vids, show=True)

    def open_dir(self, text):
        files_dir, _ = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            text,
        )
        return files_dir

    def open_files(self, text):
        # Opens a directory using File Dialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Tiff images (*.tif *.tiff);; PNG Images (*.png);; @All Files (*)",
            options=QtWidgets.QFileDialog.Options(),
        )
        return files


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, model_path):
        super(MainWindow, self).__init__()
        self.main = MainWidget(model_path)
        self.setCentralWidget(self.main)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = MainWindow(sys.argv[1])
    app.exec_()
