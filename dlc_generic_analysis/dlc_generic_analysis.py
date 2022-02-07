from qtpy import QtWidgets
from abc import abstractmethod


class MainWidget(QtWidgets.QWidget):
    def __init__(self, title: str):
        """
        The Main view of your applications where users will run analysis
        """
        super(MainWidget, self).__init__()
        self.title = title
        self.setLayout(QtWidgets.QGridLayout())
        self.title_label = QtWidgets.QLabel(self.title)
        self.layout().addWidget(self.title_label)
        self.analyze_button = QtWidgets.QPushButton("Analyze Videos")
        self.analyze_button.clicked.connect(self.on_click_analyze)
        self.layout().addWidget(self.analyze_button)
        self.view_button = QtWidgets.QPushButton("View Analyzed Video")
        self.view_button.clicked.connect(self.on_click_view)
        self.layout().addWidget(self.view_button)


    @abstractmethod
    def on_click_analyze(self):
        """
        Runs when the user clicks the analyze button
        """
        pass

    @abstractmethod
    def on_click_view(self):
        """
        Runs when the user clicks the view button
        """
        pass
