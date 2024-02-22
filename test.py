import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
from contextlib import redirect_stdout
import io

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Python Script Executor")
        
        self.layout = QVBoxLayout()
        
        self.button = QPushButton("Execute params.py")
        self.button.clicked.connect(self.execute_script)
        
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.textEdit)
        
        container = QWidget()
        container.setLayout(self.layout)
        
        self.setCentralWidget(container)
    
    def execute_script(self):
        output = io.StringIO()  # Create a string buffer to capture the output
        with redirect_stdout(output):
            try:
                with open('params.py', 'r') as file:
                    script = file.read()
                    exec(script, globals())  # Execute the script in the global namespace
            except Exception as e:
                self.textEdit.setText(f"Error executing script: {e}")
                return
        
        self.textEdit.setText(output.getvalue())  # Display the captured output in the text edit widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
