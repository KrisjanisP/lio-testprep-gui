from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtGui import QFont
from reload_label import ReloadLabelRow

class TextFileTab(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.add_reload_label()
        self.add_content_widget()

        self.setLayout(self.main_layout)

    def add_content_widget(self):
        self.content = QTextEdit()
        self.content.setReadOnly(True)
        self.content.setFont(QFont("Courier New", 12))
        self.main_layout.addWidget(self.content)

    def add_reload_label(self):
        self.reloadLabelRow = ReloadLabelRow()
        self.main_layout.addLayout(self.reloadLabelRow)

    def display_text_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                self.content.setText(file.read())
                self.reloadLabelRow.update_reload_label()
        except FileNotFoundError:
            self.content.setText(f"File not found at {file_path}.")
        except Exception as e:
            self.content.setText(str(e))