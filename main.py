import os
from PySide6.QtWidgets import QMainWindow, QApplication, QTabWidget, QMessageBox
from status_tab import StatusTab
from task_yaml_tab import TaskYamlViewerTab
from solutions_tab import SolutionsTab
from generation_tab import GenerationTab
import zipfile
import statefulness

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LIO Test Preparation GUI")
        self.resize(800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.statusTab = StatusTab(lambda task_dir:self.update_task_dir(task_dir))
        self.tabs.addTab(self.statusTab, "status")

        self.taskYamlViewerTab = TaskYamlViewerTab()
        self.tabs.addTab(self.taskYamlViewerTab, "task.yaml")

        self.generationTab = GenerationTab()
        self.tabs.addTab(self.generationTab, "generation")

        self.solutionsTab = SolutionsTab()
        self.tabs.addTab(self.solutionsTab, "solutions")

        self.task_dir = statefulness.load_last_task_dir()
        if self.task_dir:
            self.update_task_dir(self.task_dir)

    def update_task_dir(self, dir_path):
        self.task_dir = dir_path

        self.statusTab.update_task_dir(dir_path)
        self.solutionsTab.update_task_dir(dir_path)

        self.taskYamlViewerTab.load_task_yaml(dir_path)

        self.generationTab.update_task_dir(dir_path)

        statefulness.save_task_dir(dir_path)
    
    def load_tests_from_zip(self, zip_path):
        if not os.path.exists(zip_path):
            QMessageBox.warning(self, "Error", "The specified zip file does not exist.")
            return

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.task_dir)

        self.solutionsTab.update_test_data(self.task_dir)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
