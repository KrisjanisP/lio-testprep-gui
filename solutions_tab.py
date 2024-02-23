from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QTabWidget, QLabel
import os
import statefulness
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class SolutionsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.task_directory = ""
        self.solution_paths = []

        main_layout = QVBoxLayout()

        # Create a horizontal layout for the button
        button_layout = QHBoxLayout()

        # Add a spacer on the left side
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.add_sol_btn = QPushButton("Add solution")
        self.add_sol_btn.clicked.connect(self.add_solution_path)
        button_layout.addWidget(self.add_sol_btn)

        main_layout.addLayout(button_layout)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)


    def add_solution_path(self):
        if not os.path.exists(self.task_directory):
            return
        file_dialog = QFileDialog(self, "Select solution file")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec():
            new_files = file_dialog.selectedFiles()
            self.solution_paths.extend(new_files)
            statefulness.save_task_dir_solutions(self.task_directory, self.solution_paths)
            self.refresh_tabs()

    def update_task_dir(self, dir_path):
        self.task_directory = dir_path
        self.solution_paths = statefulness.load_task_dir_solutions(dir_path)
        self.refresh_tabs()

    def remove_solution_path(self, path):
        print(f"removing {path} from {self.solution_paths}")
        self.solution_paths.remove(path)
        print(f"removed {path} from {self.solution_paths}")
        statefulness.save_task_dir_solutions(self.task_directory, self.solution_paths)
        self.refresh_tabs()

    def refresh_tabs(self):
        paths = self.solution_paths
        self.tabs.clear()
        for path in paths:
            tab = QWidget()
            layout = QHBoxLayout()
            full_path_label = QLabel("Path: "+os.path.abspath(path))
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda: self.remove_solution_path([path][0]))
            layout.addWidget(full_path_label)
            layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            layout.addWidget(remove_button)

            tab.setLayout(layout)
            self.tabs.addTab(tab, os.path.basename(path))
