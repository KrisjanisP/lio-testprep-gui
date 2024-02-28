import os
import tempfile
import hashlib
import subprocess

def ensure_compiled_cpp(sol_src_path)->str:
    """
    If not yet compiled, compiles the C++ file and returns the path to the compiled executable.
    It does so by naming the executable as the sha256 of source code.
    The executable is placed in /tmp/testprep/ directory.
    """
    with open(sol_src_path, 'rb') as f:
        sol_src = f.read()
    sha256 = hashlib.sha256(sol_src).hexdigest()
    exe_path = os.path.join(tempfile.gettempdir(), 'testprep', sha256)
    if not os.path.exists(os.path.dirname(exe_path)):
        os.makedirs(os.path.dirname(exe_path))
    if not os.path.exists(exe_path):
        subprocess.run(["g++", sol_src_path, "-o", exe_path])
    return exe_path

def run_cpp_file(cpp_path, input_str, params=[]):
    """Compiles, runs and returns the stdout of a c++ file."""
    exe_path = ensure_compiled_cpp(cpp_path)
    params_str = " ".join(map(str, params))
    cmd = f"bash -c '{exe_path} {params_str}'"
    output = subprocess.check_output(cmd, input=input_str, shell=True, text=True)
    return output

def run_python_file(python_path, *args):
    """Runs a python file and returns its stdout."""
    cmd = f"python3 {python_path} {' '.join(args)}"
    output = subprocess.check_output(cmd, shell=True, text=True)
    return output