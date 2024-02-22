import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from reload_label import ReloadLabel, ReloadLabelRow

class TestsTomlTab(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.layout = QVBoxLayout()
        self.content = QTextEdit()
        self.content.setReadOnly(True)
        self.content.setStyleSheet("background-color: #f0f0f0;")
        self.reloadLabelRow = ReloadLabelRow()
        self.layout.addLayout(self.reloadLabelRow)
        self.layout.addWidget(self.content)
        self.setLayout(self.layout)

    def load_tests_toml(self):
        project_directory = self.mainWindow.project_directory
        tests_toml_path = os.path.join(project_directory, "riki", "data", "tests.toml")
        if os.path.exists(tests_toml_path):
            with open(tests_toml_path, "r") as file:
                self.content.setText(file.read())
                self.reloadLabelRow.update_reload_label()
        else:
            self.content.setText("tests.toml not found in the specified directory.")
