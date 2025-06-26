import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        # Get the full path of the provided file
        fullpath = os.path.join(working_directory, file_path)

        # Check if the directory is within the working directory
        abs_working_directory = os.path.realpath(working_directory)
        abs_fullpath = os.path.realpath(fullpath)

        # Check if the full path is outside the working directory
        if not abs_fullpath.startswith(abs_working_directory):
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"

        # Check if the path is a valid file
        if not os.path.isfile(abs_fullpath):
            return f"Error: File not found or is not a regular file: \"{file_path}\""

        MAX_CHARS = 10000
        with open(fullpath, "r") as f:
            # Read the first MAX_CHARS characters of the file
            file_content_string = f.read(MAX_CHARS)

            # Check if the content exceeds MAX_CHARS, indicating more data available
            if len(file_content_string) == MAX_CHARS:
                file_content_string += f"[...File \"{file_path}\" truncated at 10000 characters]"

        return file_content_string

    except FileNotFoundError as e:
        return f"Error: File not found: {str(e)}"
    except PermissionError as e:
        return f"Error: Permission denied: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

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