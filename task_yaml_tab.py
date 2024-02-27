import os
from text_file_tab import TextFileTab

class TaskYamlViewerTab(TextFileTab):
    def __init__(self):
        super().__init__()

    def load_task_yaml(self, task_dir):
        tests_toml_path = os.path.join(task_dir, "task.yaml")
        self.display_text_file(tests_toml_path)
