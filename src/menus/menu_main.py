import sys
from src.Discord import Discord
from src.TERMGUI.Log import Log
from src.TERMGUI.Menu import Menu
from src.FileManagement.Folder import Folder
from src.menus.menu_advanced import menu_advanced
from src.menus.menu_open_project import menu_open_category
from src.menus.menu_create_project import menu_create_project

def exit():
    Folder.clear_temp()
    # 0 = there was a problem
    # 1 = exit gracefully
    sys.exit(1)

def menu_main():
    options = [
        ["Projects",   menu_open_category],
        ["New",        menu_create_project],
        ["Advanced",   menu_advanced],
        ["Exit",       exit],
    ]

    menu = Menu(
        title   = "What would you like to do?",
        options = [ x[0] for x in options ],
        back    = False
    )

    if not options[menu.get_result()][1]():
        if not Menu.notice:
            Menu.notice = "A fatal error has occurred."

            Discord().post_log(Log.dump())

    menu_main()
