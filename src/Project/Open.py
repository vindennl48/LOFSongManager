from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder

class Open:
    def open_project(self):
        Log(f'Opening project "{self.entry.name}"..')

        # - Download any new updates / Download new project
        if self.check_for_updates():
            Log("Update to project available")
            if not self.download_and_extract():
                Log("There was a problem downloading the update..","warning")
                Log.press_enter()
                return False
        else
            return False

        Log.press_enter()

        # Check for mutex lock
        if self.is_locked():
            # Provide dialog to alert user that they can't save
            self.dialog_project_locked()

        # - Open Studio One Project
        if not self.open_studio_one():
            return False

        # Check for mutex lock
        if self.is_locked() and self.is_dirty():
            # Remove any saved changes
            Log("Removing saved data from locked project..")
            File.recursive_overwrite(
                self.get_song_file(version="original"),
                self.get_song_file()
            )
        elif self.is_dirty():
            # Lets upload our changes!
            if not self.upload_project():
                Log("An error occurred when trying to upload the project!","warning")
                Log.press_enter()
                return False

        return True

    ## HELPER FUNCS ##

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

    def open_studio_one(self):
        # Still need to make this one work

        print("OPENING STUDIO ONE")
        input()
        return True

    def upload_project(self):
        # We don't need to upload if there are no changes
        if not self.is_dirty():
            Log("There are no detected changes, can not upload!","warning")
            Log.press_enter()
            return False

        # Make sure our project is the most up-to-date
        if self.check_for_updates():
            Log("There are updates for this project on the cloud!.. can not upload!","warning")
            Log.press_enter()
            return False

        if not Dev.get("NO_OPEN_STUDIO_ONE"):
            if self.dialog_remove_unused_audio_files():
                if not self.open_studio_one():
                    return False
        else:
            Log("Development Mode prevented Studio One from opening","alert")
            Log.press_enter()

        self.compress_and_upload()

        return True

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
        dialog = Dialog(
            title = "Project is Locked!",
            body  = [
                f'This project is currently being worked on by another user!',
                f'To maintain project integrity, you will still be able to open',
                f'this project, however, you will NOT be able to save any changes!',
                f'\n',
                f'\n',
            ]
        ).press_enter()

    ## END DIALOGS ##
