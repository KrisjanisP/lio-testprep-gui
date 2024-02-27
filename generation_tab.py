import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget, QHBoxLayout, QSpacerItem, QSizePolicy,\
    QCheckBox
from tests_toml_tab import TestsTomlTab
from tests_zip_tab import TestsZipTab
from text_file_tab import TextFileTab
from export_worker import TestPreparationExportWorker
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QProgressBar
from progress_dialog import ProgressDialog

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

        self.subtask_checkboxes = []
        for i in range(1, 6):
            checkbox = QCheckBox(str(i))
            checkbox.setChecked(True)
            button_layout.addWidget(checkbox)
            self.subtask_checkboxes.append(checkbox)

        self.gen_params_btn = QPushButton("Gen params")
        self.gen_params_btn.clicked.connect(self.gen_params_clicked)
        button_layout.addWidget(self.gen_params_btn)

        self.gen_tests_btn = QPushButton("Export tests")
        self.gen_tests_btn.clicked.connect(self.export_tests_clicked)
        button_layout.addWidget(self.gen_tests_btn)

        self.main_layout.addLayout(button_layout)

    def add_tabs(self):
        self.tabs = QTabWidget()

        self.paramsPyTab = TextFileTab()
        self.tabs.addTab(self.paramsPyTab, "params.py")

        self.testsTomlTab = TestsTomlTab()
        self.tabs.addTab(self.testsTomlTab, "tests.toml")

        self.testlibGenTab = TextFileTab()
        self.tabs.addTab(self.testlibGenTab, "gen.cpp")

        self.solTab = TextFileTab()
        self.tabs.addTab(self.solTab, "sol.cpp")

        self.testsZipTab = TestsZipTab()
        self.tabs.addTab(self.testsZipTab, "tests.zip")

        self.main_layout.addWidget(self.tabs)

    def update_task_dir(self, dir_path):
        self.task_directory = dir_path
        
        params_py_path = get_params_py_path(dir_path)
        self.paramsPyTab.display_text_file(params_py_path)

        gen_cpp_path = get_generator_cpp_path(dir_path)
        self.testlibGenTab.display_text_file(gen_cpp_path)

        sol_cpp_path = get_sol_cpp_path(dir_path)
        self.solTab.display_text_file(sol_cpp_path)

        self.testsTomlTab.load_tests_toml(dir_path)

        self.testsZipTab.update_task_dir(dir_path)
        self.testsZipTab.load_tests_zip()
    
    def gen_params_clicked(self):
        print("Subtasks selected:")
        for i, checkbox in enumerate(self.subtask_checkboxes):
            if checkbox.isChecked():
                print(i+1)
    
    def export_tests_clicked(self):
        self.thread = QThread()
        self.worker = TestPreparationExportWorker(self.task_directory)
        self.worker.moveToThread(self.thread)

        self.progressDialog = ProgressDialog(self)
        self.progressDialog.show()
        
        self.worker.output.connect(self.progressDialog.add_log)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.progress.connect(self.progressDialog.update_progress)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.progressDialog.accept)  # Close the dialog when done

        
        self.thread.started.connect(self.worker.export_to_zip)
        self.thread.start()
    
    def update_result_text(self, text):
        print(text) # we will move to log area later on

def get_params_py_path(task_dir):
    return os.path.join(task_dir, "riki", "params.py")

def get_generator_cpp_path(task_dir):
    return os.path.join(task_dir, "riki", "gen.cpp")

def get_sol_cpp_path(task_dir):
    return os.path.join(task_dir, "riki", "sol.cpp")

def generate_params(task_dir):
    pass

