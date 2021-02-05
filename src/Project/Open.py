from src.Dev import Dev
from src.TERMGUI.Log import Log
from src.TERMGUI.Run import Run
from src.Settings import Settings
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder

class Open:
    def open_project(self):
        Log(f'Opening project "{self.entry.name}"..')

        # - Download any new updates / Download new project
        if not self.is_up_to_date():
            Log("Project Update Available!")
            if not self.download_project():
                Log("There was a problem downloading the update..","warning")
                Log.press_enter()
                return False
            if not self.extract_project():
                Log("There was a problem extracting the project..","warning")
                Log.press_enter()
                return False

        # Check for mutex lock
        mutex = self.is_locked()
        if mutex and mutex != Settings.get_username(capitalize=True):
            # Provide dialog to alert user that they can't save
            if not self.dialog_project_locked():
                return True
        else:
            # Lets mutex lock this beach
            self.set_lock()

        # - Open Studio One Project
        if not self.open_studio_one():
            return False

        if not self.is_remote():
            # Lets ask if user wants to upload project
            if self.dialog_upload_new_project():
                if not self.upload_project():
                    Log("An error occurred when trying to upload the project!","warning")
                    Log.press_enter()
                    return False

        elif self.is_dirty():
            # Check for mutex lock
            mutex = self.is_locked()

            if mutex and mutex != Settings.get_username(capitalize=True):
                # Project was locked by someone else
                # Remove any saved changes
                Log("Resetting project.. Undoing changes..")
                self.extract_project()
            else:
                ans = self.dialog_upload_clear_cancel()
                if ans == "y":
                    # Lets upload our changes!
                    if not self.upload_project():
                        Log("An error occurred when trying to upload the project!","warning")
                        Log.press_enter()
                        return False
                    # Remove our name from the dirty list if it exists
                    self.remove_dirty()
                elif ans == "clear":
                    self.extract_project()
                    # Remove our name from the dirty list if it exists
                    self.remove_dirty()
                else:
                    # The user is not uploading new changes..
                    # Make sure to set the project to dirty!
                    self.set_dirty()

        # Remove the lock we placed on when opening the project
        self.remove_lock()

        return True

    def create_menu_item(self):
        name   = [ self.entry.name.ljust(28)[:28] ]
        result = []

        if self.is_remote() and not self.is_local():
            name.append("- New!")
        elif self.is_remote() and self.is_local() and not self.is_up_to_date():
            name.append("- Update Available")
        elif not self.is_remote():
            name.append("- Not Uploaded")

        result.append(" ".join(name))

        if self.is_locked():
            result.append(f'          # LOCKED by {self.entry.data["is_locked"]}')
        if self.entry.data["is_dirty"]:
            result.append(f'          # NON-Uploaded changes by { ", ".join(self.entry.data["is_dirty"]) }')

        return "\n".join(result)


    ## HELPER FUNCS ##

    def open_studio_one(self):
        Log("OPENING STUDIO ONE","notice")

        # First create a temp version of the project
        File.recursive_overwrite( self.get_song_file(), self.get_song_file(version="temp") )

        Dialog(
            title = "Wait for Studio One to close!",
            body  = "DO NOT CLOSE THIS WINDOW!!"
        )

        if Dev.get("NO_OPEN_STUDIO_ONE"):
            # Do not open studio one
            return True

        # Build the dummy files
        self.set_dummy_files()

        # Open Studio One
        ans = Run.prg(
            alias   = "open",
            command = f'{ self.get_song_file(version="temp") }',
            wait    = True
        )

        # Remove dummy files
        self.remove_dummy_files()

        if ans != 0:
            return False

        # Copy over any saved data to the original song file
        File.recursive_overwrite( self.get_song_file(version="temp"), self.get_song_file() )
        File.delete( self.get_song_file(version="temp") )

        return True

    ## END HELPER FUNCS ##


    ## DIALOGS ##

    def dialog_project_locked(self):
        dialog = Dialog(
            title = f'Project is Locked by {self.entry.data["is_locked"]}!',
            body  = [
                f'This project is currently being worked on by another user!',
                f'To maintain project integrity, you will still be able to open',
                f'this project, however, you will NOT be able to save any changes!',
                f'\n', f'\n',
                f'Do you still wish to open this project?',
                f'\n', f'\n',
            ]
        )

        if dialog.get_mult_choice(["y","n"]) == "n":
            return False
        return True

    def dialog_upload_clear_cancel(self):
        result = False

        while not result:
            result = True

            dialog = Dialog(
                title = "Upload or Clear Changes!",
                body  = [
                    f'Because changes were detected, you have a couple options..',
                    f'\n', f'\n',
                    f'You can either:', f'\n',
                    f' - "y":      Upload your project to the cloud', f'\n',
                    f' - "clear":  clear any changes you recently made', f'\n',
                    f' - "cancel": keep local changes but do not upload', f'\n',
                    f'             WARNING: This will create a dirty', f'\n',
                    f'             project! May cause a loss of data', f'\n'
                    f'             in the future!',
                    f'\n', f'\n',
                ]
            )
            ans = dialog.get_mult_choice(["y","clear","cancel"])

            if ans == "clear" and not dialog.confirm():
                result = False

        return ans

    def dialog_upload_new_project(self):
        dialog = Dialog(
            title = "Upload Project!",
            body  = [
                f'You have not uploaded this project yet to the cloud..',
                f'\n', f'\n',
                f'Would you like to upload this project?',
                f'\n', f'\n',
            ]
        )
        ans = dialog.get_mult_choice(["y","n"])

        if ans == "y":
            return True
        return False

    ## END DIALOGS ##
