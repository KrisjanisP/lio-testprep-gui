import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from reload_label import ReloadLabel, ReloadLabelRow
from zipfile import ZipFile

class TestsZipTab(QWidget):
    def __init__(self):
        super().__init__()
        self.project_directory = ""

        self.layout = QVBoxLayout()

        self.labelLayout = QHBoxLayout()
        self.errorLabel = QLabel()
        self.reloadLabel = ReloadLabel()
        self.labelLayout.addWidget(self.errorLabel)
        self.labelLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.labelLayout.addWidget(self.reloadLabel)
        self.layout.addLayout(self.labelLayout)

        self.table = QTableWidget(0,3)
        self.table.setHorizontalHeaderLabels(["Test","Input","Output"])

        self.layout.addWidget(self.table)

        row = self.table.rowCount()
        self.table.insertRow(row)
        # self.table.resize()
        # self.table.resizeRowsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        self.setLayout(self.layout)

    def update_task_dir(self, dir_path):
        self.project_directory = dir_path

    def load_tests_zip(self):
        try:
            self.table.setRowCount(0)
            tests_zip_path = os.path.join(self.project_directory, "testi", "tests.zip")
            with ZipFile(tests_zip_path) as zip_ref:
                task_names = set()
                test_names = set()
                for file_info in zip_ref.infolist():
                    task_names.add(file_info.filename.split(".")[0])
                    test_name = file_info.filename.split(".")[1][1:]
                    test_names.add(test_name)
                assert len(task_names) == 1, f"Expected 1 task, found {len(task_names)}"
                task_name = task_names.pop()

                for test_name in sorted(test_names):
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    self.table.setRowHeight(row, 40)

                    self.table.setItem(row, 0, QTableWidgetItem(test_name))

                    input_file_name = f"{task_name}.i{test_name}"
                    output_file_name = f"{task_name}.o{test_name}"
                    file_info = zip_ref.getinfo(input_file_name)
                    with zip_ref.open(input_file_name, 'r') as input_file:
                        input_content = input_file.read()
                        bounded_input_content = input_content.decode('utf-8')[:150]
                        self.table.setItem(row, 1, QTableWidgetItem(bounded_input_content))
                    with zip_ref.open(output_file_name, 'r') as output_file:
                        output_content = output_file.read()
                        bounded_output_content = output_content.decode('utf-8')[:150]
                        self.table.setItem(row, 2, QTableWidgetItem(bounded_output_content))
        except Exception as e:
            self.errorLabel.setText(str(e))
        finally:
            self.reloadLabel.update_reload_label()


