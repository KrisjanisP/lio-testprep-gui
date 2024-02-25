import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtGui import QFont
from reload_label import ReloadLabelRow

class TestsTomlTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.content = QTextEdit()
        self.content.setReadOnly(True)
        self.content.setFont(QFont("Courier New", 12))
        self.reloadLabelRow = ReloadLabelRow()
        self.layout.addLayout(self.reloadLabelRow)
        self.layout.addWidget(self.content)
        self.setLayout(self.layout)

    def load_tests_toml(self, task_dir):
        tests_toml_path = os.path.join(task_dir, "riki", "data", "tests.toml")
        if os.path.exists(tests_toml_path):
            with open(tests_toml_path, "r") as file:
                self.content.setText(file.read())
                self.reloadLabelRow.update_reload_label()
        else:
            self.content.setText(f"tests.toml not found at {tests_toml_path}.")
