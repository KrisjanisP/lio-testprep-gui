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
        self.tabs.addTab(self.statusTab, "status")

        self.taskYamlViewerTab = TaskYamlViewerTab(self)
        self.tabs.addTab(self.taskYamlViewerTab, "task.yaml")

        self.testsTomlTab = TestsTomlTab(self)
        self.tabs.addTab(self.testsTomlTab, "tests.toml")

        self.solutionsTab = SolutionsTab(self)
        self.tabs.addTab(self.solutionsTab, "solutions")

        self.task_dir = load_project_directory()
        if self.task_dir:
            self.update_task_dir(self.task_dir)

    def update_task_dir(self, dir_path):
        self.task_dir = dir_path
        self.statusTab.update_task_dir(dir_path)
        self.solutionsTab.update_task_dir(dir_path)
        self.taskYamlViewerTab.load_task_yaml()
        self.testsTomlTab.load_tests_toml()
        save_project_directory(dir_path)


class SolutionsTab(QWidget):
    def __init__(self, parent:MainWindow):
        super().__init__(parent)
        self.mainWindow = parent
        self.task_directory = ""

        layout = QVBoxLayout()
        self.addButton = QPushButton("Add File")
        self.addButton.clicked.connect(self.add_solution)
        layout.addWidget(self.addButton)

        self.tabs = QTabWidget()
        self.tabs1table = QTableWidget(0, 7)
        self.tabs1table.setHorizontalHeaderLabels(["test", "group", "time", "memory", "status", "input", "output"])
        self.tabs.addTab(self.tabs1table, "tab1")

        for _ in range(100):
            row_position = self.tabs1table.rowCount()
            self.tabs1table.insertRow(row_position)
            self.tabs1table.setItem(row_position, 0, QTableWidgetItem("test1"))
            self.tabs1table.setItem(row_position, 1, QTableWidgetItem("group1"))
            self.tabs1table.setItem(row_position, 2, QTableWidgetItem("1s"))
            self.tabs1table.setItem(row_position, 3, QTableWidgetItem("256M"))
            self.tabs1table.setItem(row_position, 4, QTableWidgetItem("OK"))
            self.tabs1table.setItem(row_position, 5, QTableWidgetItem("input1"))
            self.tabs1table.setItem(row_position, 6, QTableWidgetItem("output1"))
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def update_task_dir(self, dir_path):
        self.task_directory = dir_path

    def add_solution(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select solution to add")
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
