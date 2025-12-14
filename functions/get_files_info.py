import os

def get_files_info(working_directory, directory="."):
   
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory)) 
    if os.path.isdir(target_dir):
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs 
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        try:
            with os.scandir(target_dir) as entries:
                file_struct = f""
                for entry in entries:
                    file_struct += f"- {entry.name}: file_size={os.path.getsize(entry.path)} bytes, is_dir={entry.is_dir()}\n"                    
                return file_struct
        except Exception as e:
            return f"Error: {e}"
                    
    else:
        return f'Error: "{directory}" is not a directory'