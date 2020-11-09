import time
from pathlib import Path
from src.Dev import Dev
from src.FileManagement.File import File
from src.TERMGUI.Log import Log
from src.TERMGUI.Run import Run
from src.TERMGUI.Dialog import Dialog

class Project:
    def __init__(self, folderpath):
        self.folderpath          = Path(folderpath)
        self.project             = Path(f'{self.folderpath.absolute()}/{self.folderpath.name}.song')
        self.project_temp        = Path(f'{self.folderpath.absolute()}/{self.folderpath.name}_temp.song')
        self.local_conflict      = Path(f'{self.folderpath.absolute()}/{self.folderpath.name}_yourversion.song')
        self.local_conflict_temp = Path(f'{self.folderpath.absolute()}/{self.folderpath.name}_yourversion_temp.song')

    def open_project(filepath, quiet=False, wait=True):
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

        if wait and not quiet:
            Log("Studio One has closed!")

    def open_temp(self, quiet=False, wait=True):
        if not self.project_temp.exists():
            File.recursive_overwrite(self.project, self.project_temp)

        Project.open_project(self.project_temp, quiet, wait)

        if wait:
            File.recursive_overwrite(self.project_temp, self.project)
            File.delete(self.project_temp)

    def open_conflict(self, quiet=False, wait=True):
        if not self.local_conflict_temp.exists():
            File.recursive_overwrite(self.local_conflict, self.local_conflict_temp)

        if self.local_conflict.exists():
            Project.open_project(self.local_conflict_temp, quiet, wait)

        if wait:
            File.recursive_overwrite(self.local_conflict_temp, self.local_conflict)
            File.delete(self.local_conflict_temp)

    def open_temp_and_conflict(self):
        Log("Opening Projects, please wait at least 30 seconds for both projects to open!", "notice")
        Dialog(
            title = "Please Wait!",
            body  = [
                f'Opening both projects. Please wait at least 30 seconds',
                f'before attempting to close this window!',
            ]
        )
        self.open_temp(quiet=True, wait=False)
        time.sleep(15)
        self.open_conflict()

        # this needs to still be handled since self.open_temp cant wait
        File.recursive_overwrite(self.project_temp, self.project)
        File.delete(self.project_temp)

    def open(self, wait=True):
        if self.local_conflict.exists():
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
                self.open_temp_and_conflict()
            elif ans == "2":
                self.open_temp()
            elif ans == "3":
                self.open_conflict()
            elif ans == "b":
                return False
        else:
            self.open_temp()

        return True

