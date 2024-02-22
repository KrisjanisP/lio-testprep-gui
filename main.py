import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import appdirs
import json
from reload_label import *
from status_tab import *
from task_yaml_tab import *
from tests_toml_tab import *


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
        self.testsTomlTab = TestsTomlTab(self)

        self.tabs.addTab(self.statusTab, "Status")
        self.tabs.addTab(self.taskYamlViewerTab, "task.yaml")
        self.tabs.addTab(self.testsTomlTab, "tests.toml")
        self.tabs.addTab(self.fileAdditionTab, "Add Files")

        self.project_directory = load_project_directory()
        if self.project_directory:
            self.update_project_directory(self.project_directory)

    def update_project_directory(self, dir_path):
        self.project_directory = dir_path
        self.statusTab.update_selected_directory(dir_path)
        self.taskYamlViewerTab.load_task_yaml()
        self.testsTomlTab.load_tests_toml()
        save_project_directory(dir_path)


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
