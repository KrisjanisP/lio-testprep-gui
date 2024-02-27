import os
from text_file_tab import TextFileTab

class TestsTomlTab(TextFileTab):
    def __init__(self):
        super().__init__()

    def load_tests_toml(self, task_dir):
        tests_toml_path = os.path.join(task_dir, "riki", "data", "tests.toml")
        self.display_text_file(tests_toml_path)
