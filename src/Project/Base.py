import filecmp
from pathlib import Path
from src.dev import Dev
from src.Hash import Hash
from src.Database import Entry


# Definitions
EXTRACTED          = Path("extracted_songs")
CACHED             = Path("compressed_songs")
TEMP               = Path("temp")

PROJECT_MODEL      = "projects"
DEFAULT_ENTRY_DATA = {
    "id":           None,
    "filename":     None,
    "hash":         None,
    "project_type": "new_idea",  # active, new_idea, jam, archive
    "is_locked":    None,        # If mutex is locked, user's name will show up here
    "is_dirty":     []           # List usernames of those with dirty projects
}


class Base:
    def create_from_entry(entry):
        project = Project(entry.name)
        project.entry = entry
        return project

    def __init__(self, name):
        self.entry = Entry(PROJECT_MODEL, name, DEFAULT_ENTRY_DATA)

    ## TESTS ##

    def is_dirty(self):
        # If there is locally saved changes that have yet to be uploaded to the cloud
        if Dev.get("ALL_IS_DIRTY"):
            return True

        if not self.get_song_file().exists():
            Log("Studio One project file doesn't exist!","warning")
            Log.press_enter()
            raise Exception("Studio One project file doesn't exist!")

        if not self.get_song_file(version="original").exists():
            Log("Studio One 'original' project file doesn't exist!","warning")
            Log.press_enter()
            raise Exception("Studio One 'original' project file doesn't exist!")

        return not filecmp.cmp(
            self.get_song_file(),
            self.get_song_file(version="original"),
            shallow=False
        )

    def is_up_to_date(self):
        # WE NEED A 'db.json' IN THE CACHE FOLDER WITH EXISTING HASHES
        #  Hashing these every time is extremely slow!

        # this should be in the default entry but if it's not
        if not "hash" in self.entry.data:
            self.entry.data["hash"] = None

        # If there is no hash in the entry, this means project doesnt exist on cloud
        if not self.entry.data["hash"]:
            return False

        # Compare local hash vs remote hash
        if Hash.hash_file(self.get_cache_file()) == self.entry.data["hash"]:
            return True

        # default return
        return False

    # Is this the same as 'is_up_to_date' ?
    def check_for_updates(self):
        # Return true if updates exist

        Log("Checking for updates..")

        # If project doesnt exist on cloud, no update is possible
        if not self.is_remote():
            Log("No remote files found for this project")
            # no errors, return function
            return False

        # If there is a local project, we need to check a few things
        if self.is_local():
            # If cache is already up to date, return function
            if self.is_up_to_date():
                Log("Project is already up to date!")
                return False

            if self.is_dirty():
                Log("This project is dirty with pending updates!")

                # ask if user wants to discard changes,
                # if not then do not update
                if not self.dialog_discard_changes():
                    return False

            # Remove old extracted project, lets start fresh
            Folder.delete( self.get_root_dir() )

        return True


    def is_local(self):
        # If the project is extracted to 'extracted_songs' directory
        return self.get_root_dir().exists()

    def is_cached(self):
        # If the project has a *.lof file in 'compressed_songs' directory
        return self.get_cache_file().exists()

    def is_remote(self):
        # If the project exists on the cloud yet
        if "id" in self.entry.data and self.entry.data["id"]:
            return True
        return False

    def is_locked(self):
        if "is_locked" in self.entry.data and self.entry.data["is_locked"]:
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
                f'\n',
                f'\n',
                f'This can not be undone!',
                f'\n',
                f'\n',
                f'If you would like to continue, type "yes" at the prompt.',
                f'\n',
                f'\n',
                f'If you would like to open your local project instead,',
                f'type "no" at the prompt.',
                f'\n',
                f'\n',
            ]
        )
        ans = dialog.get_mult_choice( ["yes","no"] )

        if ans == "yes":
            return True
        return False

    ## END DIALOGS ##
