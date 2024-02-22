from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from main import MainWindow

class StatusTab(QWidget):
    
    def __init__(self, parent:MainWindow):
        super().__init__(parent)
        self.mainWindow = parent
        layout = QVBoxLayout()
        self.projectStatusLabel = QLabel("No task selected")
        self.selectProjectButton = QPushButton("Select task directory")
        self.selectProjectButton.clicked.connect(self.select_project_directory)

        layout.addWidget(self.projectStatusLabel)
        layout.addWidget(self.selectProjectButton)
        self.setLayout(layout)

    def update_task_dir(self, dir_path):
        self.mainWindow.project_directory = dir_path
        self.projectStatusLabel.setText(f"Task directory: {dir_path}")

    def select_project_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if dir_path:
            self.mainWindow.update_task_dir(dir_path)
