from copy import deepcopy
from src.Database import Entry
from src.TERMGUI.Log import Log
from src.TERMGUI.Menu import Menu
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder

from src.Project.Base import Base
from src.Project.Upload import Upload
from src.Project.Download import Download
from src.Project.Extract import Extract
from src.Project.Compress import Compress
from src.Project.Open import Open
from src.Project.Dummy import Dummy
from src.Project.Delete import Delete

# Definitions
PROJECT_MODEL      = "projects"
DEFAULT_ENTRY_DATA = {
    "id":           None,
    "hash":         None,
    "project_type": "not_uploaded",  # active, new_idea, jam, archive, not_uploaded
    "is_locked":    None,            # If mutex is locked, user's name will show up here
    "is_dirty":     []               # List usernames of those with dirty projects
}


class Project(Base, Upload, Download, Extract, Compress, Open, Dummy, Delete):
    def create_from_entry(entry):
        project = Project(entry.name)
        project.entry = entry
        return project

    def __init__(self, name):
        self.entry = Entry(PROJECT_MODEL, name, deepcopy(DEFAULT_ENTRY_DATA))
        # Check to see if this already exists online
        self.entry.sync()

    def change_category(self, back=True):
        category = self.dialog_choose_category(back)
        if category:
            self.entry.data["project_type"] = category
            self.entry.update()
        return True

    def duplicate(self):
        if not self.dialog_copy_confirm():
            return False

        new_name = self.dialog_copy_new_name()
        new_path = self.get_root_dir().parent/new_name

        Log(f'Duplicating "{self.entry.name}" to "{new_name}"..')

        Folder.copy( self.get_root_dir(), new_path )

        Log(f'Renaming song file', 'sub')
        File.rename(
            new_path/(self.get_song_file().name),
            new_path/f'{new_name}.song'
        )

        if self.get_song_file(version="original").exists():
            Log(f'Renaming *original song file', 'sub')
            File.rename(
                new_path/(self.get_song_file(version="original").name),
                new_path/f'{new_name}_original.song'
            )

        Menu.notice = f'Created Project "{new_name}"!'

        return True


    ## DIALOGS ##

    def dialog_choose_category(self, back=True):
        options = [
            "active",
            "new_idea",
            "jam",
            "archive",
        ]

        menu = Menu(
            title   = f'Project "{self.entry.name}" Category | {self.entry.data["project_type"]}',
            options = options,
            back    = back
        )

        result = menu.get_result()

        if result == "back":
            return False

        return options[result]

    def dialog_copy_confirm(self):
        dialog = Dialog(
            title = f'Make Duplicate of "{self.entry.name}"',
            body  = "Would you like to make a duplicate of this project?"
        )

        ans = dialog.get_mult_choice(["y","n"])

        if ans == "y":
            return True
        else:
            return False

    def dialog_copy_new_name(self):
        dialog = Dialog(
            title = f'Make Duplicate of "{self.entry.name}"',
            body  = "Please enter a new name for your duplicate project."
        )

        new_name      = dialog.get_result("New Name").lower()
        project_names = [ x.name.lower() for x in Folder.ls_folders(self.get_root_dir().parent) ]

        if not new_name in project_names:
            return new_name

        Log("That project name already exists.. Please try again!")
        Log.press_enter()

        return self.dialog_copy_new_name()

    ## END DIALOGS ##
