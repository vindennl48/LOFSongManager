import os, subprocess
from pathlib import Path
from src.TERMGUI.Dialog import Dialog

class Run:

    alias = {
        "git": {
            "nt": f'"{Path("src/PortableGit/bin/git").absolute()}"',
            "mac": "git",
        },
        "python": {
            "nt": "python",
            "mac": "python3",
        },
        "pip": {
            "nt": "pip",
            "mac": "pip3",
        },
        "open": {
            "nt": "start",
            "mac": "open",
        },
        "clear": {
            "nt": "cls",
            "mac": "clear",
        },
        "wait": {
            "nt": "/wait",
            "mac": "-W",
        },
    }

    def prg(alias, command="", wait=False, useSubprocess=False):
        if not alias in Run.alias:
            raise Exception("Alias is not in Run.alias list!")

        wait  = Run.alias["wait"][Run.get_system()] if alias == "open" and wait else ""
        alias = Run.alias[alias][Run.get_system()]

        if useSubprocess:
            return subprocess.call(f"{alias} {wait} {command}", shell=True)

        return os.system(f"{alias} {wait} {command}")

    def ffmpeg(args, source, destination, codec=""):
        command        = []
        command_string = ""

        if os.name == 'nt':
            ffmpeg_path = Path("src/ffmpeg/bin/ffmpeg.exe")

            command = [
                f'"{ffmpeg_path.absolute()}"',
                f'{args}',
                f'"{source}"',
                f'{codec}',
                f'"{destination}"',
            ]

            command_string = " ".join(command)

            subprocess.call(command_string)

        else:
            command = [
                f'{args}',
                f'"{source}"',
                f'{codec}',
                f'"{destination}"',
            ]
            command_string = f'ffmpeg {" ".join(command)}'

            os.system(command_string)

    def get_system():
        if os.name == "nt":
            return "nt"
        return "mac"
