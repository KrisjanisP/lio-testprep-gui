from collections import defaultdict
import os
import zipfile
from PySide6.QtCore import QObject, Signal
import tomllib
from execution import run_cpp_file
import subprocess
import tempfile

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
    
        self.output.emit("Exporting tests to zip...")
        try:
            with open(toml_path, "r") as f:
                parsed_toml = tomllib.loads(f.read())
            group_test_count = defaultdict(int)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as myzip:
                tests = parsed_toml["tests"]
                for i, test_toml in enumerate(tests):
                    print(f"Exporting test {i + 1} of {len(tests)}...")

                    inp, out = gen_test_input_output(gen_path, sol_path, test_toml)
    
                    test_no = group_test_count[test_toml["group"]]
                    group_test_count[test_toml["group"]] += 1

                    i_fname, o_fname = gen_test_in_out_fnames(test_toml, test_no)
                    
                    myzip.writestr(i_fname, inp)
                    myzip.writestr(o_fname, out)

                    self.progress.emit((i + 1) / len(tests) * 100)

            self.output.emit("Exported tests to zip.")
        except Exception as e:
            self.output.emit(f"Error: {str(e)}")
        finally:
            self.finished.emit()
            self.progress.emit(0)

def gen_test_input_output(gen_path, sol_path, toml_test):
    input_str = get_test_input(toml_test, gen_path)
    output_str = run_cpp_file(sol_path, input_str)
    return input_str, output_str
    
def get_test_input(toml_test, gen_path):
    if "gen_params" in toml_test:
        gen_params = toml_test["gen_params"]
        return run_cpp_file(gen_path, "", [*gen_params])
    elif "in_from" in toml_test:
        data_dir = os.path.dirname(gen_path)
        in_from_path = os.path.join(data_dir, toml_test["in_from"])
        with open(in_from_path, "r") as f:
            return f.read()

def gen_test_in_out_fnames(toml_test, no):
    group = toml_test["group"]
    return f"dzirinas.i{str(group).zfill(2)}{chr(no + ord('a'))}",\
        f"dzirinas.o{str(group).zfill(2)}{chr(no + ord('a'))}"