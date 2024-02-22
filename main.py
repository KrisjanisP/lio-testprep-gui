import os
import yaml
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import appdirs
import json
from datetime import datetime


def get_config_path():
    # Get the appropriate user config directory for the application
    config_dir = appdirs.user_config_dir("testprep-gui", "Krišjānis Petručeņa")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)  # Create the directory if it doesn't exist
    return os.path.join(config_dir, "config.json")

def save_project_directory(project_directory):
    config_path = get_config_path()
    config = {'project_directory': project_directory}
    with open(config_path, 'w') as f:
        json.dump(config, f)

def load_project_directory():
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
            return config.get('project_directory', '')
    return ''

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LIO Test Preparation GUI")
        self.resize(800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.statusTab = StatusTab(self)
        self.taskYamlViewerTab = TaskYamlViewerTab(self)
        self.fileAdditionTab = FileAdditionTab(self)

        self.tabs.addTab(self.statusTab, "Status")
        self.tabs.addTab(self.taskYamlViewerTab, "task.yaml")
        self.tabs.addTab(self.fileAdditionTab, "Add Files")

        self.project_directory = load_project_directory()
        if self.project_directory:
            self.statusTab.update_selected_directory(self.project_directory)


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
        save_project_directory(dir_path)
        self.mainWindow.taskYamlViewerTab.load_task_yaml()

    def select_project_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if dir_path:
            self.update_selected_directory(dir_path)

class TaskYamlViewerTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.mainWindow = parent
        self.layout = QVBoxLayout()

        self.reloadLayout = QHBoxLayout()
        
        self.reloadLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.lastReloadedLabel = QLabel("Last reloaded: Never")  # Initial message
        self.reloadLayout.addWidget(self.lastReloadedLabel)

        self.taskContent = QTextEdit()
        self.taskContent.setStyleSheet("background-color: #f0f0f0;")
        self.syntaxHighlighter = YamlSyntaxHighlighter(self.taskContent.document())

        self.layout.addLayout(self.reloadLayout)
        self.layout.addWidget(self.taskContent)
        self.setLayout(self.layout)

    def load_task_yaml(self):
        project_directory = self.mainWindow.project_directory
        task_file_path = os.path.join(project_directory, "task.yaml")
        if os.path.exists(task_file_path):
            with open(task_file_path) as file:
                self.taskContent.setText(file.read())
                # Update the last reloaded label with current date and time
                now = datetime.now()
                lastReloadedText = now.strftime("Last reloaded: %Y-%m-%d %H:%M:%S")
                self.lastReloadedLabel.setText(lastReloadedText)
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

class YamlSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def highlightBlock(self, text):
        pass

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
