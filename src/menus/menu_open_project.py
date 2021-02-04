from src.TERMGUI.Log import Log
from src.TERMGUI.Menu import Menu
from src.Project.Index import Index as ProjectIndex

def menu_open_project():
    Log("Gathering projects, please wait..", "notice")

    projects = ProjectIndex.get_all_projects()

    menu = Menu(
        title   = "What project would you like to open?",
        options = [ x.create_menu_item() for x in projects ]
    )

    result = menu.get_result()

    if result == "back":
        return True
    else:
        return projects[result].open_project()
