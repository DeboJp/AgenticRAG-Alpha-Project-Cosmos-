# runner.py
import subprocess
import tempfile
import textwrap
import re

"""
Cleans up LLM output before execution
"""
def strip_markdown_fencing(code):
    return re.sub(r"```(?:python)?\n?|```", "", code).strip()

"""
Saves and runs the generated script in a temp file.
Returns stdout and stderr from the run.
"""
def run_generated_script(script_code):

    clean_code = textwrap.dedent(strip_markdown_fencing(script_code))

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(clean_code)
        temp_script_path = f.name

    print(f"\n🚀 Running generated script: {temp_script_path}\n")

    process = subprocess.run(
        ["python3", temp_script_path],
        capture_output=True,
        text=True
    )

    return process.stdout, process.stderr
