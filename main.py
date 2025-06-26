import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function, available_functions
from config import MAXITER, MODEL, SYSPROMPT, VERBOSE, VFLAG

# Loading API keys
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Creating a gemini client
client = genai.Client(api_key=api_key)

# Default values
verbose = VERBOSE

# Checking if --v flag is in the arguments
if VFLAG in sys.argv:
    verbose = True
    sys.argv.remove(VFLAG)  # Remove --v from sys.argv to avoid issues with prompt

user_prompt = ''
# Get the user prompt from command-line arguments
if len(sys.argv) > 1:
    user_prompt = sys.argv[1]  # Use the first argument as the user input
else:
    print("Please enter a prompt.")
    print("Sample: python main.py \"how does the calculator render an output?\"")
    exit(1)
    
# Sets the LLM's behavior
system_prompt = SYSPROMPT

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

# Creating message context
message = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

def generate_content():
    # Calling model
    response = client.models.generate_content(
        model=MODEL,
        contents=message,
        config=config
    )

    # Adding candidate function calls or plan of action to context
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            message.append(function_call_content)
            
    # Basic response output
    if not response.function_calls:
        return response.text

    function_responses = []
    # Checking function calls made by the LLM
    for function_call in response.function_calls:
        #print(f"Calling function: {function_call.name}({function_call.args})")
        
        # Calling the function gemini chose
        function_call_result = call_function(function_call=function_call, verbose=verbose)
        
        # Checking for a result from function_call
        if not (function_call_result.parts[0].function_response and function_call_result.parts):
            raise Exception("Fatal exception: No function result returned")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        #
        function_responses.append(function_call_result.parts[0])
        
    # If verbose mode is enabled, print the prompt
    if verbose:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count) # Response's meta data
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not function_call_result:
        raise Exception("No function response found, exiting.")
    
    message.append(types.Content(role="tool", parts=function_responses))

max_iterations = MAXITER
while max_iterations > 0:
    try:
        # Calling the LLM to generate content
        response = generate_content()
        if response:
            print(response)
            break
    except Exception as e:
        print(f"Error in generate_content(): {e}")

    max_iterations -= 1
else:
    print(f"Maximum iterations reached exiting.")
    sys.exit(1)