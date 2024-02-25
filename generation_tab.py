from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from tests_toml_tab import TestsTomlTab
from tests_zip_tab import TestsZipTab

class GenerationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.task_directory = ""
        self.solution_paths = []

        self.main_layout = QVBoxLayout()

        self.add_buttons_layout()
        self.add_tabs()

        self.setLayout(self.main_layout)

    def add_buttons_layout(self):
        button_layout = QHBoxLayout()

        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.select_param_gen_btn = QPushButton("Select param gen")
        button_layout.addWidget(self.select_param_gen_btn)

        self.select_testlib_gen_btn = QPushButton("Select testlib gen")
        button_layout.addWidget(self.select_testlib_gen_btn)

        self.gen_params_btn = QPushButton("Gen params")
        button_layout.addWidget(self.gen_params_btn)

        self.gen_tests_btn = QPushButton("Gen tests")
        button_layout.addWidget(self.gen_tests_btn)

        self.main_layout.addLayout(button_layout)
    
    def add_tabs(self):
        self.tabs = QTabWidget()

        self.testsTomlTab = TestsTomlTab()
        self.tabs.addTab(self.testsTomlTab, "tests.toml")

        self.testsZipTab = TestsZipTab()
        self.tabs.addTab(self.testsZipTab, "tests.zip")

        self.main_layout.addWidget(self.tabs)

    def update_task_dir(self, dir_path):
        self.testsTomlTab.update_task_dir(dir_path)

        self.testsZipTab.update_task_dir(dir_path)
        self.testsZipTab.load_tests_zip()