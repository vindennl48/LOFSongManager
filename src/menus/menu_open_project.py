from src.TERMGUI.Log import Log
from src.TERMGUI.Menu import Menu
from src.Project import Project

def menu_open_project():
    Log("Gathering projects, please wait..", "notice")

    projects = Project.get_all_projects()

    menu = Menu(
        title   = "What project would you like to open?",
        options = [ x.create_menu_item() for x in projects ]
    )

    result = menu.get_result()

    if result == "back":
        return True
    else:
        projects[result].open()
