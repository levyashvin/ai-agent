# Loading api keys
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')

# Creating a gemini client
from google import genai

client = genai.Client(api_key=api_key)

import sys

if len(sys.argv) > 1:
    contents = sys.argv[1:]
else:
    print('please enter a prompt')
    exit(1)

# Test response
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=contents
)
print(response.text)
# Response's meta data
print("Prompt tokens:", response.usage_metadata.prompt_token_count)
print("Response tokens:", response.usage_metadata.candidates_token_count)