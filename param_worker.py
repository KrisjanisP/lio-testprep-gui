from PySide6.QtCore import QObject, Signal
import tomllib
import os
import tempfile
import toml
import subprocess


class TestPreparationConfigurationWorker(QObject):
    finished = Signal()
    output = Signal(str)
    progress = Signal(int)
    
    def __init__(self, task_dir):
        super().__init__()
        self.task_dir = task_dir


    def configure_st_tests(self, st_list=[]):
        toml_path = os.path.join(self.task_dir, "riki", "data", "tests.toml")
        params_py_path = os.path.join(self.task_dir, "riki", "params.py")

        tests_per_group = 3

        try:
            for st_no in st_list:
                self.output.emit(f"Configuring subtask {st_no} tests...")

                with open(toml_path, "rb") as f:
                    parsed_toml = tomllib.load(f)

                st_groups = find_st_groups(parsed_toml, st_no)

                new_tests = []
                for (group_i, group) in enumerate(st_groups):
                    self.output.emit(f"Generating tests for group {st_groups[group_i]}...")

                    for i in range(tests_per_group):
                        params = run_python_file(params_py_path, str(st_no), str(group))

                        new_tests.append({
                            "group": group,
                            "gen_params": params,
                        })
                        
                        current_test_no = tests_per_group*group_i + i + 1
                        total_test_no = tests_per_group*len(st_groups)
                        progress = current_test_no / total_test_no
                        self.progress.emit(progress * 100)  # Update progress

                    self.output.emit(f"Generated tests for group {group}.")

                self.output.emit(f"Configured subtask {st_no} tests.")
                self.output.emit(f"Exporting tests to TOML...")

                new_toml = parsed_toml
                new_toml["tests"] = [*find_unrelated_tests(parsed_toml, st_groups), *new_tests]
                with open(toml_path, "w") as f:
                    f.write(toml.dumps(new_toml))
                self.output.emit(f"Exported tests to TOML.")
                
                self.output.emit(f"Configured subtask {st_no} tests.")
        except Exception as e:
            self.output.emit(f"Error: {str(e)}")
        finally:
            self.finished.emit()
            self.progress.emit(0)  # Reset progres

def run_python_file(python_path, *args):
    with tempfile.TemporaryFile() as f:
        f.write(" ".join(args).encode('utf-8'))
        f.seek(0)
        return subprocess.run(["python3", python_path], stdin=f, stdout=subprocess.PIPE).stdout.decode('utf-8')

def find_st_groups(parsed_toml, st_no):
    st_groups = []
    for group in parsed_toml["tests_groups"]:
        if group["subtask"] == st_no:
            a, b = group["groups"]
            for i in range(a,b+1):
                st_groups.append(i)
    return st_groups

def find_unrelated_tests(parsed_toml, st_groups):
    unrelated_tests = []
    for test in parsed_toml["tests"]:
        if test["group"] not in st_groups:
            unrelated_tests.append(test)
    return unrelated_tests