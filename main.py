import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file
    ]
)

def main():
    if len(sys.argv) <= 1:
        sys.exit(1)
    user_prompt = sys.argv[1]
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
            )
    )
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        metadata = dict(response.usage_metadata)
        print(f"Prompt tokens: {metadata['prompt_token_count']}")
        print(f"Response tokens: {metadata['candidates_token_count']}")
    if response.function_calls:
        for function_call in response.function_calls:
           reply = call_function(function_call, "--verbose" in sys.argv)
           if not reply.parts[0].function_response.response:
               raise Exception("Fatal Error while executing function.")
           elif not reply.parts[0].function_response.response is None and "--verbose" in sys.argv:
               print(f"-> {reply.parts[0].function_response.response}")
    if response.text:
        print(f"AI Output: {response.text.strip()}")




def call_function(function_call_part, verbose=False):
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    name = function_call_part.name
    if verbose:
        print(f"Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")

    if name == "get_file_content":
        result = get_file_content(**args)
    elif name == "get_files_info":
        result = get_files_info(**args)
    elif name == "run_python_file":
        result = run_python_file(**args)
    elif name == "write_file":
        result = write_file(**args)
    else:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    if not isinstance(result, dict):
        result = {"result": result}
    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=name,
            response=result,
        )],
    )
if __name__ == "__main__":
    main()
