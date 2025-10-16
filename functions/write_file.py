# python
# write_file.py
import os
from google import genai

schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Write to file at given file path, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(type=genai.types.Type.STRING, description="Relative path to write"),
            "content": genai.types.Schema(type=genai.types.Type.STRING, description="Content to write"),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    try:
        wd = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(wd, file_path))
        if os.path.commonpath([wd, target]) != wd:
            return {"error": f'Cannot write to "{file_path}" as it is outside the permitted working directory'}
        os.makedirs(os.path.dirname(target) or wd, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return {"file_path": file_path, "bytes_written": len(content)}
    except Exception as e:
        return {"error": str(e)}