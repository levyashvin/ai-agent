import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Loading API keys
load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')

# Creating a gemini client
client = genai.Client(api_key=api_key)

# Default values
verbose = False
verbose_flag = '--verbose'
# Checking if --v flag is in the arguments
if verbose_flag in sys.argv:
    verbose = True
    sys.argv.remove(verbose_flag)  # Remove --v from sys.argv to avoid issues with prompt

user_prompt = ''
# Get the user prompt from command-line arguments
if len(sys.argv) > 1:
    user_prompt = sys.argv[1]  # Use the first argument as the user input
else:
    print('Please enter a prompt')
    exit(1)

system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

# Creating message context
message = [types.Content(role='user', parts=[types.Part(text=user_prompt)])]

# Test response
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=message,
    config=types.GenerateContentConfig(system_instruction=system_prompt)
)
print(response.text)

# If verbose mode is enabled, print the prompt
if verbose:
    print(f"User prompt: {user_prompt}")
    # Response's meta data
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
