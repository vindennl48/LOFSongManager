from src.Dev import Dev
from src.Hash import Hash
from src.Slack import Slack
from src.Drive import Drive
from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.Folder import Folder

class Upload:
    def upload_project(self):
        # Make sure our project is the most up-to-date
        if not self.is_up_to_date():
            Log("There are updates for this project on the cloud!.. can not upload!","warning")
            Log.press_enter()
            return False

        # Make sure we set the category if it's never been uploaded before
        if not self.is_remote():
            self.change_category(back=False)

        if not Dev.get("NO_OPEN_STUDIO_ONE"):
            if self.dialog_remove_unused_audio_files():
                if not self.open_studio_one():
                    return False

        # Create folder for mixdowns on cloud if it doesnt exist
        if not Drive.get_id( self.entry.name ):
            Drive.mkdir( self.entry.name )

        if not self.compress_project():
            return False

        # Upload compressed project
        Log("Uploading.. please be patient", "notice")

        if not Dev.get("NO_LOF_UPLOAD"):
            result = Drive.upload(
                filepath = self.get_cache_file(),
                mimeType = Drive.mimeType['zip']
            )

            if not result:
                Log("Drive upload could not complete..", "warning")
                Log.press_enter()
                return False

            # Update remote hash if file was successfully uploaded
            self.entry.data["id"]   = result
            self.entry.data["hash"] = Hash.get_project_hash(self) # Hash is created in self.compress_project()
            self.entry.update()

            Slack(f'{Slack.get_nice_username()} uploaded a new version of {Slack.make_nice_project_name(self.entry.name)}')

        Log("Compression and upload complete!", "notice")

        return True

    ## DIALOGS ##

    def dialog_remove_unused_audio_files(self):
        dialog = Dialog(
            title = "Remove Unused Audio Files",
            body  = [
                f'Studio One will open and allow you to remove',
                f'unused audio files from the pool.',
                f'\n',
                f'\n',
                f'DO NOT FORGET to check the box that says to ',
                f'"Delete Files Permanently"!',
                f'\n',
                f'\n',
            ]
        )

        if dialog.get_mult_choice(["y","skip"]) == "y":
            return True
        return False

    ## END DIALOGS ##
