from src.Database import Entry

from src.Project.Base import Base
from src.Project.Upload import Upload
from src.Project.Download import Download
from src.Project.Extract import Extract
from src.Project.Compress import Compress
from src.Project.Open import Open
from src.Project.Dummy import Dummy

# Definitions
PROJECT_MODEL      = "projects"
DEFAULT_ENTRY_DATA = {
    "id":           None,
    "hash":         None,
    "project_type": "new_idea",  # active, new_idea, jam, archive
    "is_locked":    None,        # If mutex is locked, user's name will show up here
    "is_dirty":     []           # List usernames of those with dirty projects
}


class Project(Base, Upload, Download, Extract, Compress, Open, Dummy):
    def create_from_entry(entry):
        project = Project(entry.name)
        project.entry = entry
        return project

    def __init__(self, name):
        self.entry = Entry(PROJECT_MODEL, name, DEFAULT_ENTRY_DATA)
        # Check to see if this already exists online
        self.entry.sync()
