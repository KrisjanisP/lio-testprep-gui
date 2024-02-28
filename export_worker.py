from collections import defaultdict
import os
import zipfile
from PySide6.QtCore import QObject, Signal
import tomllib
import yaml
from execution import run_cpp_file

class TestPreparationExportWorker(QObject):
    finished = Signal()
    output = Signal(str)
    progress = Signal(int)  # Signal to emit progress updates

    def __init__(self, task_dir):
        super().__init__()
        self.task_dir = task_dir

    def export_to_zip(self):
        toml_path = os.path.join(self.task_dir, "riki", "data", "tests.toml")
        zip_path = os.path.join(self.task_dir, "testi", "tests.zip")
        gen_path = os.path.join(self.task_dir, "riki", "gen.cpp")
        sol_path = os.path.join(self.task_dir, "riki", "sol.cpp")
        yaml_path = os.path.join(self.task_dir, "task.yaml")
        
        self.output.emit("Exporting tests to zip...")
        try:
            with open(toml_path, "r") as f:
                parsed_toml = tomllib.loads(f.read())
            
            with open(yaml_path, "r") as f:
                parsed_yaml = yaml.load(f, Loader=yaml.FullLoader)
            
            group_test_count = defaultdict(int)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as myzip:
                tests = parsed_toml["tests"]
                for i, test_toml in enumerate(tests):
                    g_subtask = -1
                    for test_group in parsed_yaml["tests_groups"]:
                        a, b = test_group["groups"]
                        if test_toml["group"] in range(a, b + 1):
                            g_subtask = test_group["subtask"]
                            break
                    
                    test_no = group_test_count[test_toml["group"]]
                    group_test_count[test_toml["group"]] += 1
                    
                    i_fname, o_fname = gen_test_in_out_fnames(self.task_dir, test_toml, test_no)
                    if "gen_params" in test_toml:
                        self.output.emit(f"Exporting test {i_fname} (subtask {g_subtask}) with gen_params {test_toml['gen_params']}...")
                    else:
                        self.output.emit(f"Exporting test {i_fname}...")

                    inp = get_test_input(test_toml, gen_path)
                    out = run_cpp_file(sol_path, inp)
    
                    myzip.writestr(i_fname, inp)
                    myzip.writestr(o_fname, out)

                    self.progress.emit((i + 1) / len(tests) * 100)

            self.output.emit("Exported tests to zip.")
        except Exception as e:
            self.output.emit(f"Error: {str(e)}")
            print(e)
            raise e
        finally:
            self.finished.emit()
            self.progress.emit(0)

def get_test_input(toml_test, gen_path):
    if "gen_params" in toml_test:
        gen_params = toml_test["gen_params"]
        return run_cpp_file(gen_path, "", [*gen_params])
    elif "in_from" in toml_test:
        data_dir = os.path.dirname(gen_path)
        in_from_path = os.path.join(data_dir, toml_test["in_from"])
        with open(in_from_path, "r") as f:
            return f.read()

def gen_test_in_out_fnames(task_dir, toml_test, no):
    group = toml_test["group"]
    dir_name = os.path.basename(task_dir)
    return f"{dir_name}.i{str(group).zfill(2)}{chr(no + ord('a'))}",\
        f"{dir_name}.o{str(group).zfill(2)}{chr(no + ord('a'))}"