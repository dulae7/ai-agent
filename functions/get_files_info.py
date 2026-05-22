import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(working_directory_abs, directory))
        valid_target_dir = os.path.commonpath([working_directory_abs, target_directory]) == working_directory_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'
        
        for item in os.listdir(target_directory):
            item_fullpath = '/'.join([target_directory,item])
            print(f"- {item}: file_size={os.path.getsize(item_fullpath)} bytes, is_dir={os.path.isdir(item_fullpath)}")
            
        return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error: {e}"