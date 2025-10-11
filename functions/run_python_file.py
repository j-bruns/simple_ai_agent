import os
import subprocess
def run_python_file(working_directory, file_path, args=[]):
    try:      
        wd = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(wd, file_path) if not os.path.isabs(file_path) else file_path)
        if not os.path.commonpath([wd, target]) == wd:
            return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        elif not os.path.exists(target):
            return f'Error: File "{file_path}" not found.'
        elif not target.endswith(".py"):
            return(f'Error: "{file_path}" is not a Python file.')
        else:
            process = subprocess.run(["python3",target,*args],timeout=30,capture_output=True,cwd = wd)
            if process.returncode != 0:
                return f"STDOUT: {process.stdout.decode()}\nSTDERR: {process.stderr.decode()}\nProcess exited with code {process.returncode}"
            elif len(process.stdout.decode()) == 0 and len(process.stderr.decode()) == 0:
                return f"No output produced."
            else:
                return f"STDOUT: {process.stdout.decode()}\nSTDERR: {process.stderr.decode()}"
    except Exception as e:
        return(f"Error: executing Python file: {e}")