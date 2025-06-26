import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    try:
        # Ensure directory is not None, default to current working directory
        if directory is None:
            directory = ""

        # Get the full path of the provided directory
        fullpath = os.path.join(working_directory, directory)

        # Check if the directory is within the working directory
        abs_working_directory = os.path.realpath(working_directory)
        abs_fullpath = os.path.realpath(fullpath)

        # Check if the full path is outside the working directory
        if not abs_fullpath.startswith(abs_working_directory):
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"

        # Check if the full path is a valid directory
        if not os.path.isdir(fullpath):
            return f"Error: \"{directory}\" is not a directory"

        details = ""
        for item in os.listdir(fullpath):
            item_path = os.path.join(fullpath, item)

            # Get file details: size and type
            if os.path.isfile(item_path):  # Check if it's a file
                details += f"- {item}: file_size={os.path.getsize(item_path)}, is_dir=False\n"
            else:
                details += f"- {item}: is_dir=True\n"

        return details

    except Exception as e:
        return f"Error: {str(e)}"

# Function declaration for the LLM
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)