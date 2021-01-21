import os, shutil
from glob import glob
from src.dev import Dev
from pathlib import Path
from src.TERMGUI.Log import Log
from src.FileManagement.File import File

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

    def delete(folderpath):
        folderpath = Path(folderpath)
        if folderpath.exists():
            shutil.rmtree(folderpath.absolute())

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

    def ls_files(folderpath, extension=None, filename=None):
        folderpath = Path(folderpath)

        if extension:
            extension = f'.{extension}'
        else:
            extension = ""

        if not filename:
            filename = "*"

        files = glob(f"{folderpath.absolute()}/{filename}{extension}")
        files = [ Path(x) for x in files ]
        return files

    def copy(folderpath, destination):
        destination = Path(destination)
        Folder.create(destination)

        for file in Folder.ls_files(folderpath):
            File.recursive_overwrite(
                src  = file,
                dest = destination/file.name
            )
