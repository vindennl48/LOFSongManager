from copy import deepcopy
from src.Database import Entry
from src.TERMGUI.Menu import Menu

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
    "is_locked":    None,        # If mutex is locked, user's name will show up here
    "is_dirty":     []           # List usernames of those with dirty projects
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
