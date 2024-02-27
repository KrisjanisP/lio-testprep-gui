from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtGui import QFont
from reload_label import ReloadLabelRow
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
import os
from pygments import highlight

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
                filename = os.path.basename(file_path)
                file_content = file.read()
                lexer = guess_lexer_for_filename(filename, file_content)
                formatted = highlight(file_content, lexer, HtmlFormatter(style='sas', noclasses=True))
                open("test.html", "w").write(formatted)
                self.content.setHtml(formatted)
                self.reloadLabelRow.update_reload_label()
        except FileNotFoundError:
            self.content.setText(f"{os.path.basename(file_path)} not found at {file_path}.")
        except Exception as e:
            self.content.setText(str(e))