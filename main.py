import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

client = genai.Client(api_key=api_key)

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
        config = types.GenerateContentConfig(system_instruction=system_prompt)
    )
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        metadata = dict(response.usage_metadata)
        print(f"Prompt tokens: {metadata["prompt_token_count"]}")
        print(f"Response tokens: {metadata["candidates_token_count"]}")
    
    print(f"AI Output: {response.text.strip()}")

if __name__ == "__main__":
    main()
