import filecmp
from pathlib import Path
from src.Dev import Dev
from src.Hash import Hash
from src.TERMGUI.Log import Log
from src.Settings import Settings


# Definitions
EXTRACTED = Path("extracted_songs")
CACHED    = Path("compressed_songs")
TEMP      = Path("temp")


class Base:
    def is_dirty(self):
        # If there is locally saved changes that have yet to be uploaded to the cloud
        if Dev.get("ALL_IS_DIRTY"):
            return True

        if not self.get_song_file().exists():
            Log("Studio One project file doesn't exist!","warning")
            return False

        if not self.get_song_file(version="original").exists():
            Log("Studio One 'original' project file doesn't exist!","warning")
            return False

        return not filecmp.cmp(
            self.get_song_file(),
            self.get_song_file(version="original"),
            shallow=False
        )

    def is_up_to_date(self):
        # This function checks to see if the locally extracted project
        #  is the most up-to-date project
        Log("Checking for updates..")

        # If this project is no extracted, then we are not up-to-date
        if not self.is_local():
            Log("Project is not extracted")
            return False

        ## If this project is dirty, then we are up-to-date.
        ##  We don't want to accidentally overwrite our changes!
        #if self.is_dirty():
        #    Log("Project is dirty")
        #    return True

        # If there is no remote, then it is up-to-date
        if not self.is_remote():
            Log("Project is not remote")
            return True

        # If there IS remote but not local cache, we are NOT up-to-date
        if not self.is_cached():
            Log("Project is not cached")
            return False

        # If we ARE extracted, AND remote, AND cached..
        #  Lets check if the two hashes compare
        local_hash = Hash.get_project_hash(self)
        if not local_hash:
            # We will need to re-download if local hash doesnt exist still
            #  If we reach this, something went wrong and we have to re-download
            return False

        # If local and remote hashes match, we are up-to-date
        if local_hash == self.entry.data["hash"]:
            return True

        # default return
        return False

    def is_local(self):
        # If the project is extracted to 'extracted_songs' directory
        return self.get_root_dir().exists()

    def is_cached(self):
        # If the project has a *.lof file in 'compressed_songs' directory
        #  Must check if cache AND "hash" exist
        if self.get_cache_file().exists():
            if not Hash.get_project_hash(self):
                Log(f'Project "{self.entry.name}" is cached but not hashed!',"warning")
                Log.press_enter()
                return False
            Log(f'Project "{self.entry.name}" is locally cached')
            return True
        else:
            if Hash.get_project_hash(self):
                Log(f'Project "{self.entry.name}" is hashed but not cached!',"warning")
                Log.press_enter()

        Log(f'Project "{self.entry.name}" is not locally cached')
        return False

    def is_remote(self):
        # If the project exists on the cloud
        #  Must check if remote "id" AND "hash" both exist

        if self.entry.data["id"]:
            if not self.entry.data["hash"]:
                Log(f'Project "{self.entry.name}" has remote ID but not remote hash!',"warning")
                Log.press_enter()
                return False
            return True
        else:
            if self.entry.data["hash"]:
                Log(f'Project "{self.entry.name}" does not have remote ID but has remote cache!',"warning")
                Log.press_enter()

        return False

    def is_locked(self):
        if self.entry.name == "practice":
            self.entry.data["is_locked"] = "Mitch"
            # self.entry.update()
            return self.entry.data["is_locked"]
        elif "is_locked" in self.entry.data and self.entry.data["is_locked"]:
        # if "is_locked" in self.entry.data and self.entry.data["is_locked"]:
            return self.entry.data["is_locked"]
        return False

    def set_lock(self):
        # Lets mutex lock this beach
        # Only lock if there is no lock currently
        if not self.is_locked():
            self.entry.data["is_locked"] = Settings.get_username(capitalize=True)
            self.entry.update()
            return True
        return False

    def remove_lock(self):
        # Lets undo the mutex lock
        # Only unlock if we were the ones to lock it first!
        if self.is_locked() == Settings.get_username(capitalize=True):
            self.entry.data["is_locked"] = None
            self.entry.update()
            return True
        return False

    def set_dirty(self):
        username = Settings.get_username(capitalize=True)
        if username not in self.entry.data["is_dirty"]:
            self.entry.data["is_dirty"].append(username)
            self.entry.update()
            return True
        return False

    def remove_dirty(self):
        username = Settings.get_username(capitalize=True)
        if username in self.entry.data["is_dirty"]:
            self.entry.data["is_dirty"].remove(username)
            self.entry.update()
            return True
        return False


    ## END TESTS ##


    ## FILEPATHS ##

    def get_root_dir(self):
        # Get the extracted_songs directory of project
        return EXTRACTED/self.entry.name

    def get_temp_dir(self):
        # Get the temp directory of project
        return TEMP/self.entry.name

    def get_cache_file(self):
        # Get *.lof file from 'compressed_songs' directory
        return CACHED/f'{self.entry.name}.lof'

    def get_song_file(self, version=None, temp=False):
        # This function is for getting the song file for a project
        # Version Argument:
        #   Main project file: 'project.song'
        #   Original project file: 'project_original.song'
        #   Conflict project file: 'project_yourversion.song'
        #   Temp project file to open in Studio One: 'project_temp.song'
        # Temp Argument:
        #   Location of returned song file, ie.
        #   temp=False, return song file from 'extracted_songs'
        #   temp=True, return song file from 'temp'

        if not version:
            if temp:
                return self.get_temp_dir()/f'{self.entry.name}.song'
            return self.get_root_dir()/f'{self.entry.name}.song'

        if temp:
            return self.get_temp_dir()/f'{self.entry.name}_{version}.song'
        return self.get_root_dir()/f'{self.entry.name}_{version}.song'

    def get_dummy_db(self, location="Media", temp=False):
        if temp:
            return self.get_temp_dir()/location/"dummy.json"
        return self.get_root_dir()/location/"dummy.json"

    ## END FILEPATHS ##


    ## DIALOGS ##

    def dialog_discard_changes(self):
        dialog = Dialog(
            title = "Local Changes Detected!",
            body  = [
                f'There are locally saved changes that still exist!',
                f'If you continue to update, these local changes will',
                f'be erased.',
                f'\n', f'\n',
                f'This can not be undone!',
                f'\n', f'\n',
                f'If you would like to continue, type "yes" at the prompt.',
                f'\n', f'\n',
                f'If you would like to open your local project instead,',
                f'type "no" at the prompt.',
                f'\n', f'\n',
            ]
        )
        ans = dialog.get_mult_choice( ["yes","no"] )

        if ans == "yes":
            return True
        return False

    ## END DIALOGS ##
