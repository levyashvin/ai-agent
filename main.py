import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

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
# Sets the LLM's behavior
system_prompt = system_prompt = '''
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    '''

# Function declaration for the LLM
schema_get_files_info = types.FunctionDeclaration(
    name='get_files_info',
    description='Lists files in the specified directory along with their sizes, constrained to the working directory.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'directory': types.Schema(
                type=types.Type.STRING,
                description='The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.',
            ),
        },
    ),
)

# Function declaration for get_file_content
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads content from a file in the specified working directory, with a maximum of 10,000 characters. Returns an error message if the file is invalid or outside the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory to constrain the file path."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file relative to the working directory."
            ),
        }
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write data into the specified file only if it is within the working directory. If the file doesn't exist, it is created. If it exists, it is overwritten.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory to constrain the file path."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the specified file."
            ),
        }
    ),
)

# Function declaration for run_python_file
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the specified Python file within the given working directory. Ensures the file is within the allowed directory and is a valid Python file. The execution is time-limited to prevent hanging.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory where the Python file is located."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file relative to the working directory."
            ),
        }
    ),
)

# List of all the available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

# Creating message context
message = [types.Content(role='user', parts=[types.Part(text=user_prompt)])]

def generate_content():
    # Calling model
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
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
        # Response's meta data
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not function_call_result:
        raise Exception("No function response found, exiting.")
    
    message.append(types.Content(role="tool", parts=function_responses))

# Setting the maximum number of times the function can be called
max_iterations = 20

while max_iterations > 0:
    # Calling the LLm
    try:
        response = generate_content()
        if response:
            print(response)
            break
    except Exception as e:
        print(f"Error in generate_content(): {e}")
    #generate_content()
    max_iterations -= 1
else:
    print(f"Maximum iterations reached exiting.")
    sys.exit(1)