import os, shutil
from glob import glob
from src.dev import Dev
from pathlib import Path
from src.TERMGUI.Log import Log

class Folder:
    def create(folderpath, skip_if_exists=True):
        folderpath = Path(folderpath)

        if folderpath.is_file():
            Log(f'Can not create folder "{folderpath}".. This is already a file!')
        elif folderpath.is_dir():
            if skip_if_exists:
                return True
            else:
                Log(f'Can not create folder "{folderpath}".. This folder already exists!')
        else:
            os.makedirs(folderpath.absolute())
            return True

        return False

    def clear(folderpath):
        folderpath = Path(folderpath)
        if folderpath.exists():
            shutil.rmtree(folderpath.absolute())
        Folder.create(folderpath.absolute())

    def clear_temp():
        if not Dev.get("NO_CLEAR_TEMP"):
            Folder.clear("temp")
            Log("Temp directory cleared!")
        else:
            Log("Dev Mode prevented 'Folder.clear_temp' function","notice")

    def ls_folders(folderpath):
        folderpath = Path(folderpath)
        folders    = glob(f"{folderpath.absolute()}/*/")
        folders    = [ Path(x) for x in folders ]
        return folders

    def ls_files(folderpath, extension):
        folderpath = Path(folderpath)
        files = glob(f"{folderpath.absolute()}/*.{extension}")
        files = [ Path(x) for x in files ]
        return files
