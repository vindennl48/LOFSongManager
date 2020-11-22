from pathlib import Path
from src.Slack import Slack
from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder

def menu_create_project():

    dialog = Dialog(
        title = "Create New Project",
        body  = f'Would you like to create a new project?'
    )

    ans = dialog.get_mult_choice(["y","n"])

    if ans == "y":
        dialog = Dialog(
            title = "Create New Project",
            body  = f'Please create a name for your new project'
        )

        name = dialog.get_result("Name")
        name = name.replace(" ", "_").lower()

        template = Path('templates/template_01.song')
        new_song = Path(f'extracted_songs/{name}/{name}.song')

        Folder.create(new_song.parent)
        File.recursive_overwrite(template, new_song)

        Log(f'New song "{Slack.make_nice_project_name(name)}" created!', "notice")
        Log.press_enter()

        return True

    return False
