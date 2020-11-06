import os, subprocess
from pathlib import Path

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

        alias = Run.alias[alias][Run.get_system()]
        wait  = Run.alias["wait"][Run.get_system()] if alias == "open" and wait else ""

        if useSubprocess:
            return subprocess.call(f"{alias} {wait} {command}", shell=True)

        return os.system(f"{alias} {wait} {command}")

    def get_system():
        if os.name == "nt":
            return "nt"
        return "mac"
