import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        # Get the full path of the provided file
        fullpath = os.path.join(working_directory, file_path)

        # Check if the file is within the working directory
        abs_working_directory = os.path.realpath(working_directory)
        abs_fullpath = os.path.realpath(fullpath)

        # Check if the full path is outside the working directory
        if not abs_fullpath.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Open the file in write mode ('w') and write content
        with open(fullpath, 'w') as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except FileNotFoundError as e:
        return f"Error: File not found: {str(e)}"
    except PermissionError as e:
        return f"Error: Permission denied: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

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