from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QFileDialog, QWidget

class StatusTab(QWidget):
    
    def __init__(self, set_task_dir_callback):
        super().__init__()

        self.set_task_dir_callback = set_task_dir_callback
        self.task_dir = ""

        layout = QVBoxLayout()
        self.projectStatusLabel = QLabel("No task selected")
        self.selectProjectButton = QPushButton("Select task directory")
        self.selectProjectButton.clicked.connect(self.select_project_directory)

        layout.addWidget(self.projectStatusLabel)
        layout.addWidget(self.selectProjectButton)
        self.setLayout(layout)

    def update_task_dir(self, dir_path):
        self.task_dir = dir_path
        self.projectStatusLabel.setText(f"Task directory: {self.task_dir}")

    def select_project_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if dir_path:
            self.set_task_dir_callback(dir_path)
            self.update_task_dir(dir_path)
