import os
import subprocess
from google.genai import types
from config import TIMEOUT
def run_python_file(working_directory, file_path):
    try:
        # Get the full path of the provided file
        fullpath = os.path.join(working_directory, file_path)

        # Check if the directory is within the working directory
        abs_working_directory = os.path.realpath(working_directory)
        abs_fullpath = os.path.realpath(fullpath)

        # Check if the full path is outside the working directory
        if not abs_fullpath.startswith(abs_working_directory):
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"

        # Check if the path is a valid file
        if not os.path.isfile(abs_fullpath):
            return f"Error: File \"{file_path}\" not found."
        
        if not file_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file."
            
        timeout_duration = TIMEOUT  # Timeout duration in seconds

        try:
            # Run the Python script with a timeout
            result = subprocess.run(['python', abs_fullpath], capture_output=True, text=True, timeout=timeout_duration)

            print(type(result))
            print(result)
            
            output = ""

            # Handle stdout
            if result.stdout:
                output += f"STDOUT: {result.stdout}\n"
            else:
                output += "No output produced.\n"

            # Handle stderr
            if result.stderr:
                output += f"STDERR: {result.stderr}\n"

            # Check if the process exited with a non-zero code
            if result.returncode != 0:
                output += f"Process exited with code {result.returncode}\n"

            return output

        except subprocess.TimeoutExpired:
            return f"Error: The script timed out."
        except Exception as e:
            return f"Error: executing Python file: {e}"
        
    except Exception as e:
        return f"Error: {str(e)}"

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
