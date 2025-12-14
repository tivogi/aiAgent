import os 
from config import MAX_CHARS_PER_FILE

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
    