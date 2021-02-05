from src.TERMGUI.Log import Log
from src.TERMGUI.Menu import Menu
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.Folder import Folder
from src.Project.Index import Index as ProjectIndex

def menu_advanced():
    options = [
        ["Clean Out Cache",           clean_out_cache],
        ["Remove Extracted Projects", remove_extracted_projects],
    ]

    menu = Menu(
        title   = "Advanced Options",
        options = [ x[0] for x in options ]
    )

    result = menu.get_result()

    if result == "back":
        return True

    if not options[result][1]():
        return False

    return menu_advanced()

# Need a better place to put these functions
def clean_out_cache():
    dialog = Dialog(
        title = "Clean Out Cache",
        body  = [
            f'This will remove all pre-downloaded *.lof compressed files.',
            f'\n', f'\n',
            f'This should not harm any saved songs you have! This only',
            f'removes the pre-downloaded compressed cache.',
            f'\n', f'\n',
        ]
    )

    if dialog.confirm():
        Folder.clear(f'compressed_songs')
        Menu.notice = "Cache is cleaned out!"

    return True

def remove_extracted_projects():
    dialog = Dialog(
        title = "Remove Extracted Projects",
        body  = [
            f'This will remove all extracted projects from your local computer!',
            f'\n', f'\n',
            f'You have two options:',
            f'\n', f'\n',
            f'  - "all":    Remove ALL extracted projects', f'\n',
            f'  - "remote": Remove ONLY the songs that are backed up on the drive',
            f'\n', f'\n',
            f'The "remote" option will NOT delete any un-uploaded projects you have saved,',
            f'nor will either option touch ANY projects on the cloud.',
            f'\n', f'\n',
        ]
    )

    ans = dialog.get_mult_choice(["all","remote","back"])

    if ans == "back":
        return True

    if ans == "all":
        Folder.clear(f'extracted_songs')
    elif ans == "remote":
        projects = ProjectIndex.get_local_projects()
        for project in projects:
            if project.is_remote():
                Folder.delete( project.get_root_dir() )

    Menu.notice = "Extracted Projects Cleaned Out!"

    return True
