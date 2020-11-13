import sys
from src.menus.open_project import open_project
from src.TERMGUI.Menu import Menu
from src.TERMGUI.Log import Log

def exit():
    # 0 = there was a problem
    # 1 = exit gracefully
    sys.exit(1)

def main_menu():
    options = [
        ["Open", open_project],
        # ["Upload", ],
        # ["New", ],
        # ["Advanced", ],
        ["Exit", exit],
    ]

    menu = Menu(
        title   = "What would you like to do?",
        options = [ x[0] for x in options ],
        back    = False
    )

    options[menu.get_result()][1]()

    main_menu()
