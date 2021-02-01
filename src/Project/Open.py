from src.TERMGUI.Log import Log
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
        else:
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

    def open_studio_one(self):
        # Still need to make this one work

        print("OPENING STUDIO ONE")
        input()
        return True

    ## END HELPER FUNCS ##


    ## DIALOGS ##

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
