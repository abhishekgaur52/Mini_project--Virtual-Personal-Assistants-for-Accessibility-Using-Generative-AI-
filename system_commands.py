# system_commands.py
import subprocess
import platform
import psutil
from camera_helper import take_photo as take_camera_photo, open_camera_preview

# Windows-specific commands
windows_commands = {
    "calculator": "calc.exe",
    "notepad": "notepad.exe",
    "paint": "mspaint.exe",
    "cmd": "cmd.exe",
    "chrome": "chrome"  # We will use start command in Popen
}

def execute_command(user_input, context=None):
    user_input = user_input.lower()

    if platform.system() != "Windows":
        return "This command is only supported on Windows."

    # ----- Camera Context -----
    if context:
        last_app = context.get_context().get("last_app")

        # Take photo only if camera is open
        if last_app == "camera":
            if "take photo" in user_input:
                return take_camera_photo()
            if "close camera" in user_input:
                context.clear_context()
                return "Camera closed."

    # ----- Open / Close Apps -----
    for app, cmd in windows_commands.items():
        if f"open {app}" in user_input:
            try:
                if app == "chrome":
                    subprocess.Popen(["start", "chrome"], shell=True)
                else:
                    subprocess.Popen(cmd)
                if context:
                    context.set_context(app=app)
                return f"{app.capitalize()} opened."
            except Exception as e:
                return f"Cannot open {app}. ({e})"

        if f"close {app}" in user_input:
            try:
                # Terminate all processes with app name
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] and app.lower() in proc.info['name'].lower():
                        proc.terminate()
                if context:
                    context.clear_context()
                return f"{app.capitalize()} closed."
            except Exception as e:
                return f"Cannot close {app}. ({e})"

    # ----- Camera Open -----
    if "open camera" in user_input:
        if context:
            context.set_context(app="camera")
        return open_camera_preview()

    return None
