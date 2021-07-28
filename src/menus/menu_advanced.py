from src.Hash import Hash
from src.TERMGUI.Log import Log
from src.TERMGUI.Menu import Menu
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder
from src.Project.Index import Index as ProjectIndex

def menu_advanced():
    options = [
        ["Clean Out Cache",          clean_out_cache],
        ["Clear All Local Projects", clear_all_local_projects],
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

def clear_all_local_projects():
    result = Dialog(
        "Clear Local Projects",
        [
            f'This will clear all locally cached projects to save',
            f'space on your hard drive.', f'\n',
            f'This will NOT:', f'\n',
            f'  - Delete any songs on the cloud', f'\n',
            f'  - Delete any dirty projects on your computer', f'\n',
            f'    that have not been uploaded yet', f'\n',
            f'  - Remove any projects that have never been', f'\n',
            f'    uploaded to the cloud yet', f'\n',
        ]
    ).confirm()

    if result:
        for project in ProjectIndex.get_all_projects():
            if not project.is_dirty() and project.is_remote():
                # Just in case we have it locked
                project.remove_lock()

                # Remove extracted folder and cached file
                File.delete(project.get_cache_file())
                Folder.delete(project.get_root_dir())

                # Remove hash from local db
                Hash.remove_project_hash(project)

            Menu.notice = f'Local projects cleared!'
    else:
        Menu.notice = f'No local projects were cleared..'
    return True
