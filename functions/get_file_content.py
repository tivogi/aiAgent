import os 
from config import MAX_CHARS_PER_FILE
from google.genai import types

def get_file_content(working_directory, file_path):
   abs_working = os.path.abspath(working_directory)
   abs_file = os.path.abspath(os.path.join(abs_working,file_path))
   if not abs_file.startswith(abs_working):
       return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
   if not os.path.isfile(abs_file):
       return f'Error: File not found or is not a regular file: "{file_path}"'
   try:
    with open(abs_file,"r") as file:
        content = file.read(MAX_CHARS_PER_FILE)
        if len(content) == 10000:
            content += f'"{file_path}" truncated at 10000 characters'
        return content
   except Exception as e:
       return f'Error: {e}'
   

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Get up to the first 10000 characters of a file in the working directory. "
        "If the file is shorter, return the full contents. If there is an error, "
        "return a message explaining it."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)