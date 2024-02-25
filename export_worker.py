from collections import defaultdict
import os
import zipfile
from PySide6.QtCore import QObject, Signal
import tomllib
from compilation import ensure_compiled_cpp
import subprocess

class TestPreparationExportWorker(QObject):
    finished = Signal()
    output = Signal(str)
    progress = Signal(int)  # Signal to emit progress updates

    def __init__(self, toml_path, zip_path):
        super().__init__()
        self.toml_path = toml_path
        self.zip_path = zip_path

    def export_to_zip(self):
        toml_path = self.toml_path
        zip_path = self.zip_path
        self.output.emit("Exporting tests to zip...")
        try:
            with open(toml_path, "rb") as f:
                parsed_toml = tomllib.load(f)
            
            tests_in_groups = defaultdict(int)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as myzip:
                tests = parsed_toml["tests"]
                for i, test in enumerate(tests):
                    print(f"Exporting test {i + 1} of {len(tests)}...")
                    toml_dir_path = os.path.dirname(toml_path)
                    gen_path = os.path.join(toml_dir_path, "gen.cpp")
                    input_str = toml_test_input_str(toml_dir_path, gen_path, test)

                    sol_path = os.path.join(toml_dir_path, "sol.cpp")
                    output_str = run_solution(sol_path, input_str)
                    test_in_group = tests_in_groups[test["group"]]
                    tests_in_groups[test["group"]] += 1

                    # Define file names for input and output files
                    input_filename = f"dzirinas.i{str(test['group']).zfill(2)}{chr(test_in_group + ord('a'))}"
                    output_filename = f"dzirinas.o{str(test['group']).zfill(2)}{chr(test_in_group + ord('a'))}"

                    # Write input and output strings directly to the ZIP archive
                    myzip.writestr(input_filename, input_str)
                    myzip.writestr(output_filename, output_str)
                    self.progress.emit((i + 1) / len(tests) * 100)  # Update progress
            self.output.emit("Exported tests to zip.")
        except Exception as e:
            self.output.emit(f"Error: {str(e)}")
        finally:
            self.finished.emit()
            self.progress.emit(0)  # Reset progres

def run_cpp_file(sol_src_path, input_str, params=[]):
    """Compiles, runs and returns the stdout of a c++ file."""
    exe_path = ensure_compiled_cpp(sol_src_path)
    params_str = " ".join(map(str, params))
    cmd = f"bash -c '{exe_path} {params_str}'"
    output = subprocess.check_output(cmd, input=input_str, shell=True, text=True)
    return output

def get_test_input_str(toml_test, data_dir, gen_path):
    if "gen_params" in toml_test:
        gen_params = toml_test["gen_params"]
        return run_cpp_file(gen_path, data_dir, [*gen_params])
    elif "in_from" in toml_test:
        in_from_path = os.path.join(data_dir, toml_test["in_from"])
        with open(in_from_path, "r") as f:
            return f.read()

def toml_test_input_str(toml_dir_path, gen_src_rel_path, toml_test):
    if "gen_params" in toml_test:
        gen_params = toml_test["gen_params"]
        print(f"gen_params: {gen_params}")
        gen_exe_path = os.path.join(tempfile.gettempdir(), "lio_dzirinas_gen.exe")
        input_str = run_testlib_gen(gen_src_rel_path, gen_exe_path, *gen_params)
    elif "in_from" in toml_test:
        in_from_path = os.path.join(toml_dir_path, toml_test["in_from"])
        with open(in_from_path, "r") as f:
            input_str = f.read()
    return input_str

def read_toml_file(toml_path):
    with open(toml_path, "r") as file:
        return file.read()