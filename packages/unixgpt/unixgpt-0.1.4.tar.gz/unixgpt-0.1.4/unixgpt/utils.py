import subprocess
import pyperclip

def execute_unix_command(unix_command: str) -> dict:
    try:
        subprocess.run(unix_command, shell=True, check=True)
        return {"success": f"Command '{unix_command}' ran successfully."}
    except subprocess.SubprocessError as e:
        return {"error": f"Command '{unix_command}' failed to run."}
    except Exception as e:
        return {"error": f"An unexpected error occurred while executing."}


def copy_command_to_clipboard(unix_command: str) -> dict:
    try:
        pyperclip.copy(unix_command)
        return {"success": f"Command '{unix_command}' copied to clipboard successfully."}
    except pyperclip.PyperclipException:
        return {"error": f"Command '{unix_command}' was not able to be copied."} 
    except Exception as e:
        return {"error": f"An unexpected error occurred while copying."}
