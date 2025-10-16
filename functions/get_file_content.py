import os
from config import CHARACTER_LIMIT
from google import genai

schema_get_file_content = genai.types.FunctionDeclaration(
    name="get_file_content",
    description="Get file content from file at given file_path, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The file path of the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    try:
        wd = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(wd, file_path))
        if os.path.commonpath([wd, target]) != wd:
            return {"error": f'Cannot read "{file_path}" as it is outside the permitted working directory'}
        if not os.path.isfile(target):
            return {"error": f'File not found or is not a regular file: "{file_path}"'}
        with open(target, "r", encoding="utf-8") as f:
            content = f.read(CHARACTER_LIMIT)
        truncated = len(content) >= CHARACTER_LIMIT
        if truncated:
            content += f'\n[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
        return {"file_path": file_path, "content": content, "truncated": truncated}
    except Exception as e:
        return {"error": str(e)}