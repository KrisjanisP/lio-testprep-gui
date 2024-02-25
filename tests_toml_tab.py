import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from reload_label import ReloadLabelRow

class TestsTomlTab(QWidget):
    def __init__(self):
        super().__init__()
        self.task_dir = ""

        self.layout = QVBoxLayout()
        self.content = QTextEdit()
        self.content.setReadOnly(True)
        self.content.setFont(QFont("Courier New", 12))
        self.reloadLabelRow = ReloadLabelRow()
        self.layout.addLayout(self.reloadLabelRow)
        self.layout.addWidget(self.content)
        self.setLayout(self.layout)

    def update_task_dir(self, dir_path):
        self.task_dir = dir_path
        self.load_tests_toml()

    def load_tests_toml(self):
        tests_toml_path = os.path.join(self.task_dir, "riki", "data", "tests.toml")
        if os.path.exists(tests_toml_path):
            with open(tests_toml_path, "r") as file:
                self.content.setText(file.read())
                self.reloadLabelRow.update_reload_label()
        else:
            self.content.setText(f"tests.toml not found at {tests_toml_path}.")
