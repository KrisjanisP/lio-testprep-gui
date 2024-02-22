import os
import subprocess
import random
from collections import defaultdict
import tomllib # mixed type array support when loading TOML
import toml
import zipfile  # Import the zipfile module
import sys
import tempfile
from PySide6.QtWidgets import *
from PySide6.QtCore import *


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

class TestPreparationConfigurationWorker(QObject):
    finished = Signal()
    output = Signal(str)
    progress = Signal(int)  # Signal to emit progress updates

    def __init__(self, toml_path, st_list):
        super().__init__()
        self.toml_path = toml_path
        self.st_list = st_list


    def configure_st_tests(self):
        toml_path = self.toml_path

        try:
            for st_no in self.st_list:
                self.output.emit(f"Configuring subtask {st_no} tests...")

                with open(toml_path, "rb") as f:
                    parsed_toml = tomllib.load(f)

                # find subtask relevent groups
                st_groups = []
                for group in parsed_toml["tests_groups"]:
                    if group["subtask"] == st_no:
                        a, b = group["groups"]
                        for i in range(a,b+1):
                            st_groups.append(i)

                # delete previous tests
                new_tests = []
                for test in parsed_toml["tests"]:
                    if test["group"] not in st_groups:
                        new_tests.append(test)

                # generate new tests
                for group_i in range(len(st_groups)):
                    self.output.emit(f"Generating tests for group {st_groups[group_i]}...")
                    group = st_groups[group_i]
                    i = 0
                    tests_per_group = 3
                    while i<tests_per_group:
                        params = rand_st_gen_params(st_no)
                        toml_dir_path = os.path.dirname(toml_path)
                        # gen_path = os.path.join(toml_dir_path, "gen.cpp")
                        # gen_exe_path = os.path.join(tempfile.gettempdir(), "lio_dzirinas_gen.exe")
                        # gen_output = run_testlib_gen(gen_path, gen_exe_path, *params)

                        sol_path = os.path.join(toml_dir_path, "sol.cpp")
                        # sol_output = run_solution(sol_path, gen_output)
                        # if "-1" in sol_output:
                        #     if random.random() < 0.98 :
                        #         self.output.emit(f"skipping -1 output for group {group}")
                        #         continue
                        # if str(params[2]) in sol_output:
                        #     if random.random() < 0.98:
                        #         self.output.emit(f"skipping M as output for group {group}")
                        #         continue
                        # if "0" in sol_output:
                        #     if random.random() < 0.98:
                        #         self.output.emit(f"skipping 0 output for group {group}")
                        #         continue
                        new_tests.append({
                            "group": group,
                            "gen_params": params,
                        })
                        current_test_no = tests_per_group*group_i + i + 1
                        total_test_no = tests_per_group*len(st_groups)
                        progress = current_test_no / total_test_no
                        self.progress.emit(progress * 100)  # Update progress
                        i += 1
                    self.output.emit(f"Generated tests for group {group}.")
                self.output.emit(f"Configured subtask {st_no} tests.")
                self.output.emit(f"Exporting tests to TOML...")
                new_toml = parsed_toml
                new_toml["tests"] = new_tests
                with open(toml_path, "w") as f:
                    f.write(toml.dumps(new_toml))
                self.output.emit(f"Exported tests to TOML.")
                
                self.output.emit(f"Configured subtask {st_no} tests.")
        except Exception as e:
            self.output.emit(f"Error: {str(e)}")
        finally:
            self.finished.emit()
            self.progress.emit(0)  # Reset progres
    
def main():
    app = QApplication(sys.argv)
    window = TestPrepGUI()
    window.show()
    sys.exit(app.exec())

def find_parent_directory_with_name(start_path, target_dir_name):
    current_path = start_path
    while True:
        current_path, dir_name = os.path.split(current_path)
        if dir_name == target_dir_name:
            return current_path
        if not current_path or current_path == os.path.sep:
            break
    return None

def count_zero_outputs(zip_path):
    count = 0  # Initialize a counter for the files
    with zipfile.ZipFile(zip_path, 'r') as myzip:
        for file in myzip.infolist():  # Iterate through all files in the ZIP archive
            if ".o" in file.filename:
                with myzip.open(file) as f:  # Open the file for reading
                    content = f.read().decode('utf-8').strip()  # Read and decode the content
                    if content[0] == "0":  # Check if the content is exactly "0"
                        count += 1  # Increment the counter
    return count

def count_negative_one_outputs(zip_path):
    count = 0  # Initialize a counter for the files
    with zipfile.ZipFile(zip_path, 'r') as myzip:
        for file in myzip.infolist():  # Iterate through all files in the ZIP archive
            if ".o" in file.filename:
                with myzip.open(file) as f:  # Open the file for reading
                    content = f.read().decode('utf-8').strip()  # Read and decode the content
                    if content[0] == "-1":  # Check if the content is exactly "-1"
                        count += 1  # Increment the counter
    return count

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

def ensure_compiled_gen(gen_src_path, gen_exe_path):
    if not os.path.isfile(gen_exe_path) or os.path.getmtime(gen_exe_path) < os.path.getmtime(gen_src_path):
        print(f"Compiling generator from {gen_src_path} to {gen_exe_path}...")
        subprocess.run(f"g++ -std=c++17 -O2 -o {gen_exe_path} {gen_src_path}", shell=True)
        print("Finished compiling generator.")

def run_testlib_gen(gen_src_path, gen_exe_path, N, D, M, X_max, X_min, type, solvable):
    ensure_compiled_gen(gen_src_path, gen_exe_path)

    gen_params_str = " ".join(map(str, [N, D, M, X_max, X_min, type, solvable]))
    cmd = f"bash -c '{gen_exe_path} {gen_params_str}'"

    output = subprocess.check_output(cmd, shell=True, text=True)
    return output

def ensure_compiled_sol(sol_src_path, sol_exe_path):
    if not os.path.isfile(sol_exe_path) or os.path.getmtime(sol_exe_path) < os.path.getmtime(sol_src_path):
        print(f"Compiling solution from {sol_src_path} to {sol_exe_path}...")
        subprocess.run(f"g++ -std=c++17 -O2 -o {sol_exe_path} {sol_src_path}", shell=True)
        print("Finished compiling solution.")

def run_solution(sol_src_path, input_str):
    sol_exe_path = os.path.join(tempfile.gettempdir(),"lio_dzirinas_sol.exe")
    ensure_compiled_sol(sol_src_path, sol_exe_path)
    result = subprocess.run([sol_exe_path], input=input_str, text=True, capture_output=True)
    return result.stdout

def rand_st_gen_params(st_no):
    N_MAX, D_MAX, M_MAX = int(2e5), int(2e9), int(2e9)
    X_MIN, X_MAX = -int(1e9), int(1e9)
    fuzzy_p = 0.2

    if st_no == 1:
        N_MAX, D_MAX, M_MAX = 10, 10, 10
        X_MIN, X_MAX = -10, 10
        fuzzy_p = 0.8
    elif st_no == 2:
        M_MAX = 1
    elif st_no == 3:
        X_MAX = 1
    elif st_no == 4:
        N_MAX, M_MAX = int(1e3), int(1e3)
    elif st_no == 5:
        pass
    
    def f(a, b, p=fuzzy_p):
        return random.randint(a, b) if random.random() < p else b
    N = f(1, N_MAX)
    D = f(1, D_MAX)
    M = f(1, M_MAX)
    X_MAX = f(1, X_MAX)
    X_MIN = -f(1, -X_MIN)
    S = 1 if random.random() < 0.95 else 0
    P = random.choice([10, 20, 50, 80, 90])

    params = (N, D, M, X_MAX, X_MIN, S, P)
    print(f"generated params: {params}")
    return params

if __name__ == "__main__":
    main()
