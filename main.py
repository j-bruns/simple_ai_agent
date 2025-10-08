import os
import sys
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) <= 1:
        sys.exit(1)
    response = client.models.generate_content(model="gemini-2.0-flash-001",contents=sys.argv[1])
    print(response.text.strip())
    metadata = dict(response.usage_metadata)
    print(f"Prompt tokens: {metadata["prompt_token_count"]}")
    print(f"Response tokens: {metadata["candidates_token_count"]}")

if __name__ == "__main__":
    main()
