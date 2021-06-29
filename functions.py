import subprocess

from config import PLATFORM


def copy_to_clipboard(file_path: str):
    if PLATFORM == 'mac':
        subprocess.run(["osascript", "-e", f'set the clipboard to (read (POSIX file "{file_path}") '
                                           f'as JPEG picture)'])
