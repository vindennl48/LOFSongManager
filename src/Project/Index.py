from src.TERMGUI.Log import Log
from src.Database import Database
from src.Project.Base import EXTRACTED
from src.Project.Project import Project
from src.FileManagement.Folder import Folder

class Index:
    def get_all_projects():
        Log("Gathering local projects..")
        local = Index.get_local_projects()

        Log("Gathering remote projects..")
        remote   = Index.get_remote_projects()
        projects = list(remote)

        projects.extend( x for x in local if not x.is_remote() )

        return projects

    def get_local_projects():
        local = Folder.ls_folders(EXTRACTED)
        return [ Project(x.name) for x in local ]

    def get_remote_projects():
        remote = Database.get_all("projects")
        return [ Project.create_from_entry(x) for x in remote ]
