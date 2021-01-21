from src.Tar import Tar
from src.Drive import Drive
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder

class Open:
    def open_project(self):
        # - Download any new updates / Download new project
        if not self.check_for_updates():
            return False

        # Check for mutex lock
        if self.is_locked():
            # Provide dialog to alert user that they can't save
            self.dialog_project_locked()

        # - Open Studio One Project
        if not self.open_studio_one():
            return False


    ## HELPER FUNCS ##

    def check_for_updates(self):
        # If project doesnt exist on cloud, no update is possible
        if not self.is_remote():
            # no errors, return function
            return True

        # If there is a local project, we need to check a few things
        if self.is_local():
            # If cache is already up to date, return function
            if self.is_up_to_date():
                return True

            if self.is_dirty():
                # ask if user wants to discard changes,
                # if not then do not update
                if not self.dialog_discard_changes():
                    return True

            # Remove old extracted project, lets start fresh
            Folder.delete( self.get_root_dir() )

        # Download new cache
        if not Drive.download( self.entry.data["id"], self.get_cache_file() ):
            # something went wrong while downloading
            return False

        # Update cache 'db.json' with new hash

        # Clean out temp project if it exists
        Folder.delete( self.get_temp_dir() )

        # Extract cache to 'temp' folder
        Tar.extract( self.get_cache_file(), self.get_temp_dir() )

        # Create required folders in 'extracted_songs'
        self.create_required_folders()

        # Copy and convert from 'temp' to 'extracted_songs'
        if not self.move_temp_to_extracted_songs():
            # If function fails, remove broken extracted project
            # to prevent issues trying again.
            Folder.delete( self.get_root_dir() )
            return False

        return True

    def create_required_folders(self):
        # Need to make sure these folders exist
        Folder.create( self.get_root_dir()/"Media"   )
        Folder.create( self.get_root_dir()/"Bounces" )
        Folder.create( self.get_root_dir()/"Mixdown" )

    def move_temp_to_extracted_songs(self):
        # Convert mp3's to wav's
        if not Audio.folder_to_wav( self.get_temp_dir()/"Media", self.get_root_dir()/"Media" ):
            return False
        if not Audio.folder_to_wav( self.get_temp_dir()/"Bounces", self.get_root_dir()/"Bounces" ):
            return False

        # Copy over the previous mixdowns
        Folder.copy( self.get_temp_dir()/"Mixdown", self.get_root_dir()/"Mixdown" )

        # Copy over the song file
        File.recursive_overwrite( self.get_song_file(temp=True), self.get_song_file(temp=False) )

    def open_studio_one(self):
        pass

    ## END HELPER FUNCS ##


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

    def dialog_project_locked(self):
        pass

    ## END DIALOGS ##
