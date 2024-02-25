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
    if not os.path.exists(exe_path):
        subprocess.run(["g++", sol_src_path, "-o", exe_path])
    return exe_path
    