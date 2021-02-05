# UPGRADE TO V1.1

# this is required to access 'src' modules
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir  = os.path.dirname(currentdir)
sys.path.append(parentdir)
##########################################

from src.Settings import Settings
from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.File import File

if __name__ == "__main__":
    # Before we finish the update, we need to update the core files
    if not Settings.get_key("update_git"):
        Settings.set_key("update_git",True)

        dialog = Dialog(
            title = "Upgrading to V1.3!",
            body  = [
                f'Welcome to a new friendly update!  Hopefully everything goes nice',
                f'and smooth, haha! .... #justkiddingbutseriously',
                f'\n', f'\n',
                f'The main fix for this update solves the slow-down issues while trying',
                f'to open up a project.',
                f'\n', f'\n',
                f'There also was some significant code improvements on both local and remote',
                f'servers to allow for new features, yay!  Features such', f'\n',
                f'as:', f'\n',
                f'  - Locking projects if they are open by another user', f'\n',
                f'  - Seeing who has a project open.', f'\n',
                f'  - Adding a category to projects to start sorting between jams, active songs, ideas, etc.', f'\n',
                f'  - And much more!', f'\n',
                f'\n', f'\n',
                f'For more information, please refer to the repository commits and/or the slack channel.',
                f'\n', f'\n',
            ]
        )
        dialog.press_enter()

        # Rename src/dev.py to src/Dev.py
        File.rename("src/dev.py", "src/Dev.py")

        Log("A restart is needed to update the core!","notice")
        Log("Please ignore the following error message and restart the program.","sub")
        Log.press_enter()
        # 0 = there was a problem upgrading
        # 1 = do not restart core
        # 2 = restart core is necessary
        sys.exit(0)

    dialog = Dialog(
        title = "Upgrading to V1.3!",
        body  = [
            f'Lets go ahead and finish this dang update, shall we?!',
            f'\n',
            f'\n',
        ]
    )
    dialog.press_enter()

    # Now that we have updated the core, we can continue with the rest of the update!
    Settings.delete_key("update_git")

    # Remove 'env.py' in favor of .settings file
    File.delete("src/env.py")

    # Remove 'user' key from .settings
    Settings.delete_key("user")

    # 0 = there was a problem upgrading
    # 1 = do not restart core
    # 2 = restart core is necessary
    sys.exit(2)
