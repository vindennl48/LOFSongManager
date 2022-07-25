from src.Dev import Dev
from src.Hash import Hash
from src.Discord import Discord
from src.Drive import Drive
from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.File import File
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

        # We will need to set the local hash on our own incase of failure
        #  to upload
        if not self.compress_project(set_hash=False):
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

            # Update local hash
            Hash.set_project_hash(self, Hash.create_hash_from_project(self))

            # Update remote hash if file was successfully uploaded
            self.entry.data["id"]   = result
            self.entry.data["hash"] = Hash.get_project_hash(self)
            self.entry.update()

            # Send an upload notification to Discord
            username     = Settings.get_username(capitalize = True)
            project_name = f'"{self.entry.name.replace("_"," ")}"'.capitalize()
            content      = f"{username} uploaded a new version of {nice_name}"
            Discord().post_message(content)

            # Remove name from dirty list
            self.remove_dirty()

            # Since we successfully uploaded to the drive, we can now get
            #  rid of the *original song file
            File.recursive_overwrite( self.get_song_file(), self.get_song_file(version="original") )

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
