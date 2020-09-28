from src.helpers import *

def create_new_project(main_menu):
    clear_screen()
    display_title("Would you like to create a new project?")

    if input(":: (y/n): ") != "y":
        return False

    name = None
    while not name:
        log("Please type a name for your new project")
        name = input(":: Project Name: ")

    template = Path('templates/template_01.song')
    new_song = Path(f'extracted_songs/{name}/{name}.song')

    mkdir(new_song.parent)
    recursive_overwrite(template, new_song)

    log(f"New song '{name}' created!")
    pause()

    return True
