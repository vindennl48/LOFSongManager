import os
from pathlib import Path
from src.dev import Dev
from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog


class Tar:
    def compress(folderpath, destination):
        folderpath  = Path(folderpath)
        destination = Path(destination)
        cwd         = Path.cwd()

        Log(f'Compressing "{folderpath.stem}"..')

        if not Dev.get("NO_COMPRESS"):
            try:
                os.system(f'cd "{folderpath.parent}" && tar -czf "{destination.absolute()}" "{folderpath.name}" && cd "{cwd.absolute()}"')
            except Exception as e:
                Log(f'Failed to compress "{folderpath.stem}"')
                Log(f'\n\n{e}\n\n', None)
                Log.press_enter()
                exit()

        Log(f'Finished compressing "{folderpath.stem}!"')

    def extract(filepath, destination):
        filepath    = Path(filepath)
        destination = Path(destination)

        Log(f'Extracting "{filepath.stem}"..')

        if not Dev.get("NO_EXTRACT"):
            try:
                os.system(f"tar -xzf {filepath.absolute()} -C {destination.absolute()}")
            except Exception as e:
                Log(f'Failed to extract "{filepath.stem}"')
                Log(f'\n\n{e}\n\n', None)
                Log.press_enter()
                exit()

        Log(f'Finished extracting "{filepath.stem}!"')
