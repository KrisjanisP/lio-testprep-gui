import os
import yaml
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QTableWidget, QTableWidgetItem, QHBoxLayout
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Manager")
        self.resize(800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.statusTab = StatusTab(self)
        self.taskViewerTab = TaskYamlViewerTab(self)
        self.fileAdditionTab = FileAdditionTab(self)

        self.tabs.addTab(self.statusTab, "Status")
        self.tabs.addTab(self.taskViewerTab, "task.yaml")
        self.tabs.addTab(self.fileAdditionTab, "Add Files")

        self.project_directory = ""

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

    def select_project_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if dir_path:
            self.mainWindow.project_directory = dir_path
            self.projectStatusLabel.setText(f"Project Directory: {dir_path}")
            self.mainWindow.taskViewerTab.load_task_yaml()

class TaskYamlViewerTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWindow = parent
        self.layout = QVBoxLayout()
        self.taskContent = QTextEdit()
        self.taskContent.setReadOnly(True)
        self.layout.addWidget(self.taskContent)
        self.setLayout(self.layout)

    def load_task_yaml(self):
        project_directory = self.mainWindow.project_directory
        task_file_path = os.path.join(project_directory, "task.yaml")
        if os.path.exists(task_file_path):
            with open(task_file_path) as file:
                self.taskContent.setText(file.read())
        else:
            self.taskContent.setText("task.yaml not found in the selected directory.")

class FileAdditionTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWindow = parent
        layout = QHBoxLayout()
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["File Name", "File Size (KB)"])
        self.addButton = QPushButton("Add File")
        self.addButton.clicked.connect(self.add_file)

        layout.addWidget(self.table)
        layout.addWidget(self.addButton)
        self.setLayout(layout)

    def add_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file to add")
        if file_path:
            file_info = os.stat(file_path)
            file_size = file_info.st_size // 1024
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(os.path.basename(file_path)))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(file_size)))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()