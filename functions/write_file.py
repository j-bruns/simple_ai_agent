import os
def write_file(working_directory, file_path, content):
        try:      
            wd = os.path.abspath(working_directory)
            target = os.path.abspath(os.path.join(wd, file_path) if not os.path.isabs(file_path) else file_path)
            if not target.startswith(wd):
                return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
            else:
                os.makedirs(os.path.dirname(target),exist_ok=True) 
                with open(target, "w") as f:
                    f.write(content)
                return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
        except Exception as e:
            return f"Error: {e}"