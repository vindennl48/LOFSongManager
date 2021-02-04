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

        # Check for mutex lock
        if self.is_locked():
            # Provide dialog to alert user that they can't save
            if not self.dialog_project_locked():
                return True

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
            ans = self.dialog_upload_clear_cancel()

            if ans == "upload":
                # Lets upload our changes!
                if not self.upload_project():
                    Log("An error occurred when trying to upload the project!","warning")
                    Log.press_enter()
                    return False
            elif ans == "clear":
                Folder.delete(self.get_root_dir())

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
        # Still need to make this one work

        print("OPENING STUDIO ONE")
        input()
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
                    f' - Upload your project to the cloud', f'\n',
                    f' - Clear any changes you recently made', f'\n',
                    f' - Cancel, keep local changes but do not upload', f'\n',
                    f'   WARNING: This will create a dirty project! May', f'\n',
                    f'            cause a loss of data in the future!',
                    f'\n', f'\n',
                ]
            )
            ans = dialog.get_mult_choice(["upload","clear","cancel"])

            if ans == "clear" and not dialog.confirm():
                result = False

        return ans

    ## END DIALOGS ##
