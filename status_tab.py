from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class StatusTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWindow = parent
        layout = QVBoxLayout()
        self.projectStatusLabel = QLabel("No project selected")
        self.selectProjectButton = QPushButton("Select Project Directory")
        self.selectProjectButton.clicked.connect(self.select_project_directory)

        layout.addWidget(self.projectStatusLabel)
        layout.addWidget(self.selectProjectButton)
        self.setLayout(layout)

    def update_selected_directory(self, dir_path):
        self.mainWindow.project_directory = dir_path
        self.projectStatusLabel.setText(f"Project Directory: {dir_path}")

    def select_project_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if dir_path:
            self.update_selected_directory(dir_path)
