from src.helpers import *
from src.menus.extract import extract
from src.menus.compress import compress
from src.menus.exit_program import exit_program
from src.menus.update_program import update_program


## MAIN MENU
def main_menu():
    # Create default file structure if it doesnt exist
    mkdir("compressed_songs")
    mkdir("extracted_songs")
    mkdir("temp")
    mkdir("templates")

    clear_screen()
    display_title("What would you like to do?")

    menu_items = [
        ["Extract Project",  extract],
        ["Compress Project", compress],
        ["Update",           update_program],
        ["Exit",             exit_program],
    ]
    ans = list_options(menu_items)
    menu_items[ans][1](main_menu)

    main_menu()




