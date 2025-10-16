import os
from google import genai

schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The directory to list from, relative to the working directory. Defaults to '.'",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        wd = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(wd, directory))
        if os.path.commonpath([wd, target]) != wd:
            return {"error": f'Cannot list "{directory}" as it is outside the permitted working directory'}
        if not os.path.isdir(target):
            return {"error": f'"{directory}" is not a directory'}
        items = []
        for name in os.listdir(target):
            path = os.path.join(target, name)
            items.append({
                "name": name,
                "is_dir": os.path.isdir(path),
                "size": os.path.getsize(path) if os.path.isfile(path) else None,
            })
        return {"directory": directory, "items": items}
    except Exception as e:
        return {"error": str(e)}