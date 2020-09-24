from src.helpers import *
from src.menus.exit_program import exit_program

def update_program(main_menu):
    clear_screen()

    display_title("Updates")

    log("Checking for updates..")
    git_update()
    log("Update Complete!")

    pause()
    exit_program(main_menu)
