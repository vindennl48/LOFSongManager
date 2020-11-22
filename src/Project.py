import time, filecmp
from glob import glob
from pathlib import Path
from src.Dev import Dev
from src.Audio import Audio
from src.DummyFiles import DummyFiles
from src.Drive import Drive
from src.env import LOFSM_DIR_PATH, LOFSM_DIR_HASH
from src.Hash import Hash
from src.Tar import Tar
from src.Slack import Slack
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
        self.dummy            = DummyFiles(f'{self._extracted_path()}')
        self.did_notify       = False
        self.drive            = Drive()

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
        if self.drive.get_info(self.remote):
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

        elif not self.is_recent() and self.is_remote():
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

    def _clear_conflict(self):
        File.delete(self.yourversion)

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

        if not self._update():
            return False

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
                self._open_temp_and_yourversion()
            elif ans == "2":
                self._open_yourversion()
            elif ans == "3":
                self._open_temp()
            elif ans == "b":
                return False
        else:
            self._open_temp()

        return True

    def _update(self):
        if not self.is_recent() and self.is_remote():
            if self.song.exists():
                Log("Update available!", "notice")

            if self.yourversion.exists():
                dialog = Dialog(
                    title = "A Conflict Still Exists!",
                    body  = [
                        f'A conflict still exists in this project.  We can',
                        f'not update your project until this conflict gets',
                        f'resolved!',
                        f'\n',
                        f'\n',
                        f'If you are certain that this conflict was already',
                        f'taken care of, press "y".',
                        f'\n',
                        f'\n',
                        f'If you need some more time to resolve the conflict,',
                        f'press "n"',
                        f'\n',
                        f'\n',
                    ], clear=False
                )

                ans = dialog.get_mult_choice("y","n")

                if ans == "n":
                    return False

                self._clear_conflict()

            Log("Downloading.. please be patient", "notice")

            result = self.drive.download(
                ID        = self.drive.get_info(self.remote),
                save_path = self.compressed
            )

            if not result:
                Log("Drive download could not complete..", "warning")
                Log.press_enter()
                return False

            self._unpack()

        return True

    def _unpack(self):
        # convert compressed project to extracted project
        Folder.clear_temp()
        Tar.extract(
            filepath    = self.compressed,
            destination = Project.temp_parent
        )

        if self.song.exists() and self.song_original.exists():
            if not filecmp.cmp(self.song, self.song_original, shallow=False):
                dialog = Dialog(
                    title = "Local changes found!",
                    body  = [
                        f'When local changes are detected, this software will',
                        f'generate a conflict file.  You must open both projects',
                        f'and copy all of your changes to the newly downloaded',
                        f'project.',
                        f'\n',
                        f'\n',
                        f'To prevent this from happening in the future, make sure',
                        f'you always have the most up-to-date project BEFORE making',
                        f'changes, and make sure you push your project to the cloud',
                        f'as soon as you are finished!',
                        f'\n',
                        f'\n',
                    ]
                )
                dialog.press_enter()

                File.recursive_overwrite(
                    src  = self.song,
                    dest = self.yourversion
                )

        # Copy over song files
        Folder.create(self._extracted_path())
        File.recursive_overwrite(
            src  = f'{self._temp_path()}/{self.song.name}',
            dest = self.song
        )
        File.recursive_overwrite(
            src  = f'{self._temp_path()}/{self.song.name}',
            dest = self.song_original
        )

        # Copy over the rest
        for path in glob(f"{self._temp_path()}/*"):
            path   = Path(path)
            result = True

            if path.name == "Media":
                result = Audio.folder_to_wav(
                    folderpath  = path,
                    destination = f'{self._extracted_path()}/Media/'
                )
                DummyFiles(f'{self._extracted_path()}/Media/')

            elif path.name == "Bounces":
                result = Audio.folder_to_wav(
                    folderpath  = path,
                    destination = f'{self._extracted_path()}/Bounces/'
                )
                DummyFiles(f'{self._extracted_path()}/Bounces/')

            elif path.suffix == ".song":
                pass  ## Ignore

            else:
                File.recursive_overwrite(path, f'{self.song.parent}/{path.name}')

        if not result:
            return False

        Folder.clear_temp()

        return True


    ## Private ##
    def _open_temp(self, quiet=False, wait=True):
        if not self.song_temp.exists():
            File.recursive_overwrite(self.song, self.song_temp)

        self._open_project(self.song_temp, quiet, wait)

        if wait:
            self._close_temp()

    def _close_temp(self):
        if not Dev.get("NO_OPEN_STUDIO_ONE"):
            File.recursive_overwrite(self.song_temp, self.song)
            File.delete(self.song_temp)

    def _open_yourversion(self, quiet=False, wait=True):
        if not self.yourversion_temp.exists():
            File.recursive_overwrite(self.yourversion, self.yourversion_temp)

        if self.yourversion.exists():
            self._open_project(self.yourversion_temp, quiet, wait)

        if wait:
            self._close_yourversion()

    def _close_yourversion(self):
        if not Dev.get("NO_OPEN_STUDIO_ONE"):
            File.recursive_overwrite(self.yourversion_temp, self.yourversion)
            File.delete(self.yourversion_temp)

    def _open_temp_and_yourversion(self):
        Dialog(
            title = "Please Wait!",
            body  = [
                f'Opening both projects. Please wait at least 30 seconds',
                f'before attempting to close this window!',
            ]
        )
        self._open_temp(quiet=True, wait=False)
        time.sleep(15)
        self._open_yourversion()

        # this needs to still be handled since self.open_temp cant wait
        self._close_temp()

    def _open_project(self, filepath, quiet=False, wait=True):
        filepath = Path(filepath)

        if not self.did_notify:
            Slack(f'{Slack.get_nice_username()} is working on {Slack.make_nice_project_name(self.name)}', endpoint="dev")
            self.did_notify = True

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

