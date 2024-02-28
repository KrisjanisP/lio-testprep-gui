from PySide6.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QTextEdit

class ProgressDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)  # Assuming 100 steps. Adjust accordingly.
        layout.addWidget(self.progressBar)

        self.logTextEdit = QTextEdit(self)
        self.logTextEdit.setReadOnly(True)
        layout.addWidget(self.logTextEdit)

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def add_log(self, message):
        # Append log message and ensure it's visible
        self.logTextEdit.append(message)
        self.logTextEdit.ensureCursorVisible()
