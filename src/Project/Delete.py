from src.Hash import Hash
from src.Drive import Drive
from src.TERMGUI.Menu import Menu
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder

class Delete:
    def delete_project(self):
        options = []
        if self.is_local():
            options.append("local")
        if self.is_remote():
            options.append("remote")
        if self.is_local() and self.is_remote():
            options.append("both")
        options.append("back")

        dialog = Dialog(
            title = f'Deleting Project "{self.entry.name}"',
            body  = [
                f'Would you like to delete the local or remote version?',
                f'\n', f'\n',
                f'Warning: This is not reversible!',
            ]
        )

        ans = dialog.get_mult_choice(options)

        if ans == "back":
            return True

        if ans == "local" or ans == "both":
            # Remove extracted folder and cached file
            File.delete(self.get_cache_file())
            Folder.delete(self.get_root_dir())

            # Remove hash from local db
            Hash.remove_project_hash(self)

            Menu.notice = f'Project "{self.entry.name}" deleted locally!'

        if ans == "remote" or ans == "both":
            if self.is_remote():
                # Delete compressed file
                project_id = self.entry.data["id"]
                if project_id:
                    Drive.delete(project_id)

                # Delete folder with scratch tracks and mixdowns
                folder_id = Drive.get_id(self.entry.name)
                if folder_id:
                    Drive.delete(folder_id)

                # Remove entry from remote db
                self.entry.destroy()

                Menu.notice = f'Project "{self.entry.name}" deleted remotely!'

        if ans == "both":
            Menu.notice = f'Project "{self.entry.name}" completely deleted!'

        return True
