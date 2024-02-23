import os
import appdirs
import json

# on linux $HOME/.config/testprep-gui/config.json
def get_config_path():
    """Get the appropriate user config JSON path for the application"""
    config_dir = appdirs.user_config_dir("testprep-gui", "Krišjānis Petručeņa")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return os.path.join(config_dir, "config.json")

def save_task_dir(project_directory):
    config_path = get_config_path()
    config = {'project_directory': project_directory}
    with open(config_path, 'w') as f:
        json.dump(config, f)

def load_last_task_dir():
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
            return config.get('project_directory', '')
    return ''