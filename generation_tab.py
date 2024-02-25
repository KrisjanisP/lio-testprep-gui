import hashlib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QTabWidget, QLabel
import os
import statefulness
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from tests_toml_tab import *
from tests_zip_tab import *

class GenerationTab(QWidget):
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
        button_layout.addWidget(self.add_sol_btn)

        main_layout.addLayout(button_layout)

        self.tabs = QTabWidget()

        self.testsTomlTab = TestsTomlTab()
        self.tabs.addTab(self.testsTomlTab, "tests.toml")

        self.testsZipTab = TestsZipTab()
        self.tabs.addTab(self.testsZipTab, "tests.zip")

        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def update_task_dir(self, dir_path):
        self.testsTomlTab.update_task_dir(dir_path)

        self.testsZipTab.update_task_dir(dir_path)
        self.testsZipTab.load_tests_zip()