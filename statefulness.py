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

def load_config() -> dict:
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    raise FileNotFoundError(f"Config file not found at {config_path}")

def save_config(config: dict):
    config_path = get_config_path()
    with open(config_path, 'w') as f:
        json.dump(config, f)

def save_task_dir(task_dir):
    config = load_config()
    config['project_directory'] = task_dir
    save_config(config)

def load_last_task_dir():
    return load_config().get('project_directory')

def save_task_dir_solutions(task_dir, sol_paths):
    config = load_config()
    config['sol_paths'][task_dir] = sol_paths
    save_config(config)

def load_last_task_dir_solution_paths(task_dir):
    return load_config().get('sol_paths', {}).get(task_dir, [])

def save_sol_test_results(task_dir, sol_code_sha256, results):
    config = load_config()
    config['sol_test_results'][task_dir][sol_code_sha256] = results
    save_config(config)

def load_sol_test_results(task_dir, sol_code_sha256):
    return load_config().get('sol_test_results', {}).get(task_dir, {}).get(sol_code_sha256, [])