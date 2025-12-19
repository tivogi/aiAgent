import os
import argparse
from prompts import system_prompt
from call_function import call_function
from functions.call_function import available_functions
from dotenv import load_dotenv
from google import genai
from google.genai import types


def generate_content(client,messages,verbose):
    function_responses = []
    
    content = client.models.generate_content(model="gemini-2.5-flash",
                                                contents=messages,
                                                config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
))
    if not content:
        raise RuntimeError("API failed request")
    
    if verbose:
        print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
    
    if content.function_calls:
        for function_call_part in content.function_calls:
            try: 
                function_call_result = call_function(function_call_part, verbose=verbose)

                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                    or function_call_result.parts[0].function_response.response is None
                ):
                    raise RuntimeError("Function call did not return a function_response")

                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                function_responses.append(function_call_result.parts[0])
                print(f"{function_call_part.name}")
            except Exception as e:
                raise e
        
    else:
        print(f"Response:")
        print(content.text) 
    
    if function_responses:
        messages.append(types.Content(role="user", parts=function_responses))   
    
    if content.function_calls and not function_responses:
        raise Exception("no function responses generated, exiting.")

    

    return function_responses,content   
   

    


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        client = genai.Client(api_key=api_key)
        parser = argparse.ArgumentParser(description="Chatbot")
        parser.add_argument("user_prompt", type=str,help="User prompt")
        parser.add_argument("--verbose", action="store_true",  help="Enable verbose output")
        args = parser.parse_args()
        messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
      
        count = 0
        while count <= 20: 
            try:
                response,content = generate_content(client,messages,args.verbose)
            except Exception as e:
                print(e)
                break
            for candidate in content.candidates:
                messages.append(candidate.content)
            if not content.function_calls and content.text:
                print(content.text)
                break
            count += 1
        
    else:
        raise RuntimeError("There's no valid API key")

if __name__ == "__main__":
    main()

