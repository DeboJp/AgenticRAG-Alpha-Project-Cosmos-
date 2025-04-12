# runner.py
import importlib.util, sys
import os
import tempfile

"""
Saves and runs the generated script in a temp file.
Returns stdout and stderr from the run.
"""
def run_tool(path):
    print(f"\n🚀 Running tool file: {path}\n")

    if not os.path.exists(path):
        print("❌ File not found.")
        return
    
    tool_dir = os.path.dirname(os.path.abspath(path))
    sys.path.insert(0, tool_dir)  # ← ✅ Make sibling imports resolvable

    # Dynamically load and run the module
    spec = importlib.util.spec_from_file_location("tool", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)