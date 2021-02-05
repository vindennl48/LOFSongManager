from src.TERMGUI.Log import Log
from src.TERMGUI.Menu import Menu
from src.Project.Index import Index as ProjectIndex

def menu_open_category():
    # This function will allow the user to sort betweein different
    # project types. (categories / tags / etc.)

    options = [
        "all",
        "active",
        "new_idea",
        "jam",
        "archive",
        "not_uploaded",
    ]

    menu = Menu(
        title   = "Filter By Category",
        options = options
    )

    result = menu.get_result()

    if result == "back":
        return True
    else:
        if not menu_open_project( filter=options[result] ):
            return False
        else:
            return menu_open_category()


def menu_open_project(filter="active"):
    # The filter argument will sort between categoried projects
    # If "all" is passed, all songs will show up
    # If "active" is passed, only songs that are categorized with "active"
    #  in the "project_type" entry field will show up.

    Log("Gathering projects, please wait..", "notice")

    projects = ProjectIndex.get_all_projects()
    if filter != "all":
        projects = [ x for x in projects if x.entry.data["project_type"] == filter ]

    menu = Menu(
        title   = "What project would you like to select?",
        options = [ x.create_menu_item() for x in projects ]
    )

    result = menu.get_result()

    if result == "back":
        return True
    else:
        return menu_project_options(projects[result])


def menu_project_options(project):
    options = []

    options.append(["Open", project.open_project])
    # options.append(["Change Name", None])
    # options.append(["Duplicate", None])

    if not project.is_remote():
        options.append(["Upload", project.upload_project])
    else:
        options.append(["Change Category", project.change_category])

    options.append(["Delete", project.delete_project])


    menu = Menu(
        title   = f'Project "{project.entry.name}"',
        options = [ x[0] for x in options ]
    )

    result = menu.get_result()

    if result == "back":
        return True
    else:
        if options[result][0] == "Delete":
            return options[result][1]()

        if not options[result][1]():
            return False

        return menu_project_options(project)
