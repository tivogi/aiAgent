import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str,help="User prompt")
    parser.add_argument("--verbose", action="store_true",  help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    content = client.models.generate_content(model="gemini-2.5-flash",
                                             contents=messages)
    if args.verbose: 
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
        print(content.text)
    elif content:
        print(content.text)
    else:
        RuntimeError("API failed request")
else:
    RuntimeError("There's no valid API key")

