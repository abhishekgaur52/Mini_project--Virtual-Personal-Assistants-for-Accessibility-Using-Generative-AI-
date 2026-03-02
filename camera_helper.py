import os
import subprocess


def open_camera_preview():
    try:
        os.system("start microsoft.windows.camera:")
        return "Windows camera opened."
    except Exception as e:
        return f"Failed to open camera. ({e})"


def take_photo():
    return "Please click the capture button in the Camera app."


def close_camera():
    try:
        subprocess.call("taskkill /IM WindowsCamera.exe /F", shell=True)
        return "Camera closed."
    except Exception as e:
        return f"Failed to close camera. ({e})"