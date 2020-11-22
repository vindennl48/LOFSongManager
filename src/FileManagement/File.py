import json, os, shutil, re, filecmp
from pathlib import Path
from src.TERMGUI.Log import Log
from src.FileManagement.FileEdit import FileEdit

class File(FileEdit):
    def recursive_overwrite(src, dest, ignore=None):
        # taken from: https://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all
        if os.path.isdir(src):
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(src)
            if ignore is not None:
                ignored = ignore(src, files)
            else:
                ignored = set()
            for f in files:
                if f not in ignored:
                    File.recursive_overwrite(os.path.join(src, f),
                                             os.path.join(dest, f),
                                             ignore)
        else:
            src  = Path(src)
            dest = Path(dest)

            Log(f'Copying "{src.name}" to "{dest.name}"..')
            if dest.exists():
                if not filecmp.cmp(src.absolute(), dest.absolute(), shallow=False):
                    Log(f'Older duplicate found! Overwriting file "{dest.name}"', "blank")
                else:
                    Log(f'Keeping original file "{dest.name}"', "sub")
                    return False

            shutil.copyfile(src, dest)
            return True

    def split_name(filepath):
        # This splits a filename 'Mitch(23).wav' into
        # [ "Mitch", 23 ] or 'Mitch(REC)(26).wav' into
        # [ "Mitch(REC)", 26 ]
        file       = Path(filepath).name
        file, ext  = file.split(".")
        file_array = file.split("(")
        num        = re.findall(r"(\d+)\)", file_array[-1])
        num        = int(num[0]) if len(num) > 0 else 0
        file_stem  = ""

        if num > 0:
            file_array.pop()
        file_stem = "(".join(file_array)

        return [ file_stem, num, ext ]


    def get_json(filepath):
        filepath = Path(filepath)
        result   = None

        if filepath.exists():
            with open(filepath.absolute()) as f:
                result = json.load(f)

        return result

    def set_json(filepath, data):
        filepath = Path(filepath)

        with open(filepath.absolute(), "w") as f:
            json.dump(data, f, indent=4)

    def set_json_key(filepath, key, data):
        json_file      = File.get_json(filepath)
        json_file[key] = data
        File.set_json(filepath, json_file)

    def get_json_key(filepath, key):
        json_file = File.get_json(filepath)
        if not key in json_file:
            return None
        return json_file[key]
