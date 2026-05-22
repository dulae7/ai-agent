import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path where the file python will be run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                 type=types.Type.STRING   
                ),
                description="Additional argument will be added to command python that will be run",
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)
        
        completed_proc = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output = ""

        if completed_proc.returncode != 0:
            output += "Process exited with code X"
        elif completed_proc.stdout == None and completed_proc.stderr == None:
            output += "No output produced"
        else:
            output += f"STDOUT: {completed_proc.stdout} STDERR: {completed_proc.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"