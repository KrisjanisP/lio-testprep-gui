import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class SolutionsTab(QWidget):
    def __init__(self, parent):
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

    def update_test_data(self, dir_path):
        # Clear existing rows
        self.tabs1table.setRowCount(0)

        # Iterate over files in the task directory
        for filename in os.listdir(dir_path):
            if filename.endswith(".i") or filename.endswith(".o"):
                # Parse the filename to extract test details
                name, ext = os.path.splitext(filename)
                group, test_no_char = name.split('.')[-1][0], name.split('.')[-1][1:]
                file_type = 'input' if 'i' in ext else 'output'
                # Assuming time, memory, and status are not in the file and need to be set manually or are static
                time, memory, status = "1s", "256M", "OK"
                content = "input content" if file_type == 'input' else "output content"
                
                # Add a new row to the table for each file
                row_position = self.tabs1table.rowCount()
                self.tabs1table.insertRow(row_position)
                self.tabs1table.setItem(row_position, 0, QTableWidgetItem(test_no_char))
                self.tabs1table.setItem(row_position, 1, QTableWidgetItem(group))
                self.tabs1table.setItem(row_position, 2, QTableWidgetItem(time))
                self.tabs1table.setItem(row_position, 3, QTableWidgetItem(memory))
                self.tabs1table.setItem(row_position, 4, QTableWidgetItem(status))
                self.tabs1table.setItem(row_position, 5, QTableWidgetItem("input" if file_type == 'input' else ""))
                self.tabs1table.setItem(row_position, 6, QTableWidgetItem("output" if file_type == 'output' else ""))

    def add_solution(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select solution to add")
        if file_path:
            file_info = os.stat(file_path)
            file_size = file_info.st_size // 1024
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(os.path.basename(file_path)))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(file_size)))