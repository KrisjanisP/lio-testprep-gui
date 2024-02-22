import os
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class TestPrepGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Preparation GUI")
        self.setGeometry(100, 100, 800, 600)  # Adjust size as needed for 4K resolution
        
        self.subtask_checkboxes = []
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Input fields for TOML and ZIP paths
        self.input_label = QLabel("Input paths:")
        self.layout.addWidget(self.input_label)
        self.setup_path_input()

        start_path = os.getcwd()
        target_dir_name = "3_valsts"
        root_dir = find_parent_directory_with_name(start_path, target_dir_name)
        root_dir = f"{root_dir}/{target_dir_name}"
        
        toml_path_root = f"{root_dir}/dzirinas/riki/task.toml"
        zip_path_root = f"{root_dir}/dzirinas/riki/dist/tests.zip"

        if os.path.exists(toml_path_root):
            self.toml_path_entry.setText(toml_path_root)
        if os.path.exists(zip_path_root):
            self.zip_path_entry.setText(zip_path_root)

        # Buttons for actions
        self.setup_subtask_conf_section()
        self.setup_action_buttons()

        # Add a progress bar
        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)
        # Initialize the progress bar
        self.progress_bar.setMaximum(100)  # Assuming 100% is the max value
        self.progress_bar.setValue(0)  # Start with 0% progress

        # Result display area
        self.logs_label = QLabel("Logs:")
        self.layout.addWidget(self.logs_label)
        self.setup_result_display()

        # add button to clear result text
        self.clear_result_button_layout = QHBoxLayout()
        self.clear_result_button = QPushButton("Clear logs")
        self.clear_result_button.clicked.connect(self.clear_result_text)
        self.clear_result_button_layout.addStretch(1)
        self.clear_result_button_layout.addWidget(self.clear_result_button)
        self.layout.addLayout(self.clear_result_button_layout)


    def setup_subtask_conf_section(self):
        self.subtask_label = QLabel("Select Subtasks:")

        # Container for checkboxes
        self.subtask_layout = QHBoxLayout()
        self.subtask_layout.addWidget(self.subtask_label)
        self.subtask_checkboxes = []
        for i in range(1, 6):
            checkbox = QCheckBox(str(i))
            checkbox.setChecked(True)
            self.subtask_layout.addWidget(checkbox)
            self.subtask_checkboxes.append(checkbox)
        self.subtask_layout.addStretch(1)
        self.configure_tests_button = QPushButton("Configure Tests")
        self.configure_tests_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.configure_tests_button.clicked.connect(self.configure_tests)
        self.subtask_layout.addWidget(self.configure_tests_button, 100)

        self.layout.addLayout(self.subtask_layout)

    def setup_path_input(self):
        # TOML path input
        toml_layout = QHBoxLayout()
        self.toml_path_entry = QLineEdit()
        self.toml_browse_button = QPushButton("Browse...")
        self.toml_browse_button.clicked.connect(lambda: self.browse_file(self.toml_path_entry))
        toml_layout.addWidget(QLabel("TOML Path:"))
        toml_layout.addWidget(self.toml_path_entry)
        toml_layout.addWidget(self.toml_browse_button)
        self.layout.addLayout(toml_layout)

        # ZIP path input
        zip_layout = QHBoxLayout()
        self.zip_path_entry = QLineEdit()
        self.zip_browse_button = QPushButton("Browse...")
        self.zip_browse_button.clicked.connect(lambda: self.browse_file(self.zip_path_entry, save=True))
        zip_layout.addWidget(QLabel("ZIP Path:"))
        zip_layout.addWidget(self.zip_path_entry)
        zip_layout.addWidget(self.zip_browse_button)
        self.layout.addLayout(zip_layout)

    def generate_yaml(self):
        self.update_result_text("Generating YAML...")
        with open('task.yaml.temp', 'r') as f:
            yaml_template = f.read()


    def setup_action_buttons(self):
        self.export_zip_button = QPushButton("Export to ZIP")
        self.export_zip_button.clicked.connect(self.export_zip)
        self.count_outputs_button = QPushButton("Count Outputs")
        self.count_outputs_button.clicked.connect(self.count_outputs)
        self.generate_yaml_button = QPushButton("Generate YAML")
        self.generate_yaml_button.clicked.connect(self.generate_yaml)
        
        self.layout.addWidget(self.export_zip_button)
        self.layout.addWidget(self.count_outputs_button)
        self.layout.addWidget(self.generate_yaml_button)

    def setup_result_display(self):
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

    def browse_file(self, line_edit, save=False):
        if save:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "ZIP files (*.zip)")
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "TOML files (*.toml)")
        if file_path:
            line_edit.setText(file_path)

    def configure_tests(self):
        self.thread = QThread()
        subtasks = [i + 1 for i, checkbox in enumerate(self.subtask_checkboxes) if checkbox.isChecked()]
        self.worker = TestPreparationConfigurationWorker(self.toml_path_entry.text(), subtasks)
        self.worker.moveToThread(self.thread)

        self.worker.output.connect(self.update_result_text)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.started.connect(self.worker.configure_st_tests)
        self.thread.start()

    def export_zip(self):
        self.thread = QThread()
        self.worker = TestPreparationExportWorker(self.toml_path_entry.text(), self.zip_path_entry.text())
        self.worker.moveToThread(self.thread)

        self.worker.output.connect(self.update_result_text)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.started.connect(self.worker.export_to_zip)
        self.thread.start()

    def update_result_text(self, text):
        self.result_text.append(text)
    
    def clear_result_text(self):
        self.result_text.clear()

def main():
    app = QApplication(sys.argv)
    window = TestPrepGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()