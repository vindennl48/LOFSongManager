import os
from pathlib import Path
from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog


class Tar:
    def compress(filepath, destination):
        filepath    = Path(filepath)
        destination = Path(destination)
        cwd         = Path.cwd()

        Log(f'Compressing "{filepath.stem}"..')

        try:
            os.system(f'cd "{filepath.parent}" && tar -czf "{destination.absolute()}" "{filepath.name}" && cd "{cwd.absolute()}"')
        except Exception as e:
            Log(f'Failed to compress "{filepath.stem}"')
            Log(f'\n\n{e}\n\n', None)
            Log.press_enter()
            exit()

        Log(f'Finished compressing "{filepath.stem}!"')

    def extract(filepath, destination):
        filepath    = Path(filepath)
        destination = Path(destination)

        Log(f'Extracting "{filepath.stem}"..')

        try:
            os.system(f"tar -xzf {filepath.absolute()} -C {destination.absolute()}")
        except Exception as e:
            Log(f'Failed to extract "{filepath.stem}"')
            Log(f'\n\n{e}\n\n', None)
            Log.press_enter()
            exit()

        Log(f'Finished extracting "{filepath.stem}!"')
