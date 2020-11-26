from pathlib import Path
from src.Slack import Slack
from src.Drive import Drive
from src.Project import Project
from src.TERMGUI.Log import Log
from src.TERMGUI.Menu import Menu
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder

def menu_delete_project():

    projects = Project.get_all_projects()

    menu = Menu(
        title   = "What project would you like to delete?",
        options = [ x.name for x in projects ]
    )

    ans = menu.get_result()

    if ans == "back":
        return True

    project = projects[ans]

    dialog = Dialog(
        title = "What project would you like to delete?",
        body  = [
            f'Would you like to delete the local or remote version?',
            f'\n',
            f'\n',
            f'Warning: This is not reversible!',
        ]
    )

    ans = dialog.get_mult_choice(["local","remote","both","back"])

    if ans != "back" and dialog.confirm():
        if ans == "local" or ans == "both":
            File.delete(project.compressed)
            Folder.delete(project._extracted_path())
            Menu.notice = f'Project "{project.name}" deleted locally!'

        if ans == "remote" or ans == "both":
            ID = project.is_remote()
            if ID:
                Drive().delete(ID)
            project.hash.remove()
            Menu.notice = f'Project "{project.name}" deleted remotely!'

        return True

    Log("Returning to previous menu..","notice")
    return menu_delete_project()
