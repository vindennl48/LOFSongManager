import time, filecmp
from pathlib import Path
from src.Dev import Dev
from src.Drive import Drive
from src.env import LOFSM_DIR_PATH, LOFSM_DIR_HASH
from src.Hash import Hash
from src.TERMGUI.Log import Log
from src.TERMGUI.Run import Run
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder

class Project:

    # Local extracted project path
    extracted_parent  = "extracted_songs"
    # Local compressed project path
    compressed_parent = "compressed_songs"
    # Local temp project path
    temp_parent       = "temp"

    def __init__(self, name):
        name_split = name.split(".")
        if name_split[-1] == "lof":
            name = name.split(".")[0]

        self.name             = name
        self.song             = Path(f'{self._extracted_path()}/{name}.song')
        self.song_temp        = Path(f'{self._extracted_path()}/{name}_temp.song')
        self.song_original    = Path(f'{self._extracted_path()}/{name}_original.song')
        self.yourversion      = Path(f'{self._extracted_path()}/{name}_yourversion.song')
        self.yourversion_temp = Path(f'{self._extracted_path()}/{name}_yourversion_temp.song')
        self.compressed       = Path(f'{self._compressed_path()}/{name}.lof')
        self.remote           = f'{LOFSM_DIR_PATH}/{self.name}.lof'
        self.hash             = Hash(self.compressed)

    def is_dirty(self):
        if self.song.exists() and self.song_original.exists():
            return not filecmp.cmp(self.song.absolute(), self.song_original.absolute(), shallow=False)
        return False

    def is_recent(self):
        return self.hash.compare()

    def is_local(self):
        return Path(self._extracted_path()).exists()

    def is_cached(self):
        return self.compressed.exists()

    def is_remote(self):
        if Drive().get_info(self.remote):
            return True
        return False

    def create_menu_item(self):
        result = [ self.name.ljust(30)[:30] ]
        flags  = {
            "new":             "- New",
            "update":          "- Update",
            "update_conflict": "- Update (Conflict!)",
            "not_uploaded":    "- Not Uploaded",
            "dirty":           "- Dirty",
        }

        if not self.is_cached():
            if self.is_remote():
                result.append(flags["new"])
            else:
                result.append(flags["not_uploaded"])

        elif not self.is_recent():
            if self.is_dirty():
                result.append(flags["update_conflict"])
            else:
                result.append(flags["update"])

        elif self.is_dirty():
            result.append(flags["dirty"])

        return " ".join(result)

    ## Private ##
    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    def _extracted_path(self):
        return f'{Project.extracted_parent}/{self.name}'

    def _compressed_path(self):
        return f'{Project.compressed_parent}'

    def _temp_path(self):
        return f'{Project.temp_parent}/{self.name}'

    ## Static ##
    def get_local_projects():
        return [ Project(x.name) for x in Folder.ls_folders(Project.extracted_parent) ]

    def get_remote_projects():
        drive_projects = Drive().ls(search=LOFSM_DIR_HASH)
        return [ Project(x["name"]) for x in drive_projects if x['mimeType'] == Drive.mimeType['zip'] ]

    def get_all_projects():
        local_projects  = Project.get_local_projects()
        remote_projects = Project.get_remote_projects()
        projects        = list(local_projects)

        projects.extend(x for x in remote_projects if x not in projects)

        return projects


##################################################
## Opening Projects 
##################################################
    def open(self):
        if self.yourversion.exists():
            dialog = Dialog(
                title = "A Conflict Exists in This Project!",
                body  = [
                    f'This occurs when changes to a local project fall behind',
                    f'the version that is currently in the cloud.',
                    f'\n',
                    f'\n',
                    f'Would you like to:',
                    f'\n',
                    f'  1) Open both?',
                    f'\n',
                    f'  2) Open your last saved version?',
                    f'\n',
                    f'  3) Open the most recent cloud version?',
                    f'\n',
                    f'\n',
                    f'  b) back',
                    f'\n',
                    f'\n',
                ]
            )
            ans = dialog.get_mult_choice(["1","2","3","b"])

            if ans == "1":
                self._open_temp_and_conflict()
            elif ans == "2":
                self._open_temp()
            elif ans == "3":
                self._open_conflict()
            elif ans == "b":
                return False
        else:
            self._open_temp()

        return True

    ## Private ##
    def _open_temp(self, quiet=False, wait=True):
        if not self.song_temp.exists():
            File.recursive_overwrite(self.song, self.song_temp)

        Project._open_project(self.song_temp, quiet, wait)

        if wait:
            self._close_temp()

    def _close_temp(self):
        if not Dev.get("NO_OPEN_STUDIO_ONE"):
            File.recursive_overwrite(self.song_temp, self.song)
            File.delete(self.song_temp)

    def _open_conflict(self, quiet=False, wait=True):
        if not self.yourversion_temp.exists():
            File.recursive_overwrite(self.yourversion, self.yourversion_temp)

        if self.yourversion.exists():
            Project._open_project(self.yourversion_temp, quiet, wait)

        if wait:
            self._close_temp()

    def _close_conflict(self):
        if not Dev.get("NO_OPEN_STUDIO_ONE"):
            File.recursive_overwrite(self.yourversion_temp, self.yourversion)
            File.delete(self.yourversion_temp)

    def _open_temp_and_conflict(self):
        Log("Opening Projects, please wait at least 30 seconds for both projects to open!", "notice")
        Dialog(
            title = "Please Wait!",
            body  = [
                f'Opening both projects. Please wait at least 30 seconds',
                f'before attempting to close this window!',
            ]
        )
        self._open_temp(quiet=True, wait=False)
        time.sleep(15)
        self._open_conflict()

        # this needs to still be handled since self.open_temp cant wait
        self._close_temp()

    ## Static / Private ##
    def _open_project(filepath, quiet=False, wait=True):
        filepath = Path(filepath)

        if not quiet:
            Dialog(
                title = "Wait for Studio One to close!",
                body  = "DO NOT CLOSE THIS WINDOW!!"
            )

        if not Dev.get("NO_OPEN_STUDIO_ONE"):
            Run.prg(
                alias   = "open",
                command = f'{filepath.absolute()}',
                wait    = wait
            )
        else:
            Log("Development Mode prevented Studio One from opening", "alert")
            Log.press_enter()

        if wait and not quiet:
            Log("Studio One has closed!")

