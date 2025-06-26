import re
import os
from google.genai import types

def search_in_file(working_directory, file_path, search_pattern, is_regex=False):
    """
    Searches for a string or regex pattern in a given file.

    Args:
        working_directory (str): The directory to constrain the file path.
        file_path (str): The relative file path.
        search_pattern (str): The string or regex pattern to search for.
        is_regex (bool): Flag to determine if the pattern is a regex pattern. Defaults to False (string search).

    Returns:
        list: A list of matching lines or a message if no matches are found.
    """
    try:
        # Get the full path of the provided file
        fullpath = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.realpath(working_directory)
        abs_fullpath = os.path.realpath(fullpath)

        # Check if the file is within the working directory
        if not abs_fullpath.startswith(abs_working_directory):
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"

        # Check if the path is a valid file
        if not os.path.isfile(abs_fullpath):
            return f"Error: File not found or is not a regular file: \"{file_path}\""

        matches = []
        with open(fullpath, "r") as file:
            for line_number, line in enumerate(file, start=1):
                # If regex is True, use regex matching
                if is_regex:
                    if re.search(search_pattern, line):
                        matches.append(f"Line {line_number}: {line.strip()}")
                else:
                    if search_pattern in line:
                        matches.append(f"Line {line_number}: {line.strip()}")

        # If matches are found, return the matches, otherwise return "No matches found."
        if matches:
            return matches
        else:
            return ["No matches found."]
    
    except FileNotFoundError as e:
        return f"Error: File not found: {str(e)}"
    except PermissionError as e:
        return f"Error: Permission denied: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

# Function declaration for search_in_file
schema_search_in_file = types.FunctionDeclaration(
    name="search_in_file",
    description="Searches for a string or regex pattern in a file within the specified working directory.",
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
            "search_pattern": types.Schema(
                type=types.Type.STRING,
                description="The string or regex pattern to search for."
            ),
            "is_regex": types.Schema(
                type=types.Type.BOOLEAN,
                description="Flag to determine if the pattern is a regex pattern."
            ),
        }
    ),
)