import os
import functools

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory,directory)
        print(full_path)
        if not working_directory in os.path.abspath(full_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        lines = []
        for file in os.listdir(full_path):
            lines.append(f"- {file}: file_size={os.path.getsize(f"{full_path}/{file}")} bytes, is_dir={os.path.isdir(f"{full_path}/{file}")}")
        return functools.reduce(lambda line1,line2: f"{line1}\n{line2}",lines)
    except Exception as e:
         return f"Error {e}"