import os
from config import CHARACTER_LIMIT
def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory,file_path)
        if not working_directory in os.path.abspath(full_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(full_path, "r") as f:
                file_content_string = f.read(CHARACTER_LIMIT)
                if len(file_content_string) == CHARACTER_LIMIT:
                    file_content_string += f"\n[...File \"{file_path}\" truncated at 10000 characters]"
                return file_content_string
    except Exception as e:
        return f"Error: {e}"
