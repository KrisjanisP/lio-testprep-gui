from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import statefulness
import os

class SolutionsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.task_directory = ""
        self.solution_paths = []

        layout = QVBoxLayout()

        self.add_sol_btn = QPushButton("Add solution")
        self.add_sol_btn.clicked.connect(self.add_solution_path)
        layout.addWidget(self.add_sol_btn)
        
        self.setLayout(layout)

    def add_solution_path(self):
        if not os.path.exists(self.task_directory):
            return
        file_dialog = QFileDialog(self, "Select solution file")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec():
            self.solution_paths.extend(file_dialog.selectedFiles())
            statefulness.save_task_dir_solutions(self.task_directory, self.solution_paths)

    def update_task_dir(self, dir_path):
        self.task_directory = dir_path
        self.solution_paths = statefulness.load_task_dir_solutions(dir_path)
