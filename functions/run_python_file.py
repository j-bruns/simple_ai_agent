import os
import subprocess
from google import genai

schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file with optional arguments, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(type=genai.types.Type.STRING, description="Relative Python file path"),
            "args": genai.types.Schema(
                type=genai.types.Type.ARRAY,
                items=genai.types.Schema(type=genai.types.Type.STRING),
                description="Optional CLI arguments",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        args = args or []
        wd = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(wd, file_path))
        if os.path.commonpath([wd, target]) != wd:
            return {"error": f'Cannot execute "{file_path}" as it is outside the permitted working directory'}
        if not os.path.exists(target):
            return {"error": f'File "{file_path}" not found.'}
        if not target.endswith(".py"):
            return {"error": f'"{file_path}" is not a Python file.'}
        proc = subprocess.run(
            ["python3", target, *args],
            timeout=30,
            capture_output=True,
            cwd=wd,
            text=True,
        )
        return {
            "file_path": file_path,
            "args": args,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except Exception as e:
        return {"error": f"executing Python file: {e}"}