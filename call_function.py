from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file
from config import WORKDIR
# List of all the available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

#  funciton_call is a types.FunctionCall type
def call_function(function_call, verbose=False):
    # Setting working directory
    working_directory = WORKDIR
        
    # Print args if verbose true
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
        
    # Sictionary of usable function name to function
    function_map = {
        'get_file_content': get_file_content,
        'write_file': write_file,
        'run_python_file': run_python_file,
        'get_files_info': get_files_info,
    }    
    
    if function_call.name in function_map:
        # Adding the working directory to the function_call's args dictionary
        function_args = {**function_call.args, "working_directory": working_directory}
        
        # Calling the function
        function_result = function_map[function_call.name](**function_args)
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )
    