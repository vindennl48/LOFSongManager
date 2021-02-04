# UPGRADE TO V1.1

# this is required to access 'src' modules
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir  = os.path.dirname(currentdir)
sys.path.append(parentdir)
##########################################

from src.Settings import Settings
from src.TERMGUI.Dialog import Dialog
from src.FileManagement.File import File

if __name__ == "__main__":
    dialog = Dialog(
        title = "Upgrading to V1.3!",
        body  = [
            f'Welcome to a new friendly update!  Hopefully everything goes nice',
            f'and smooth, haha! .... #justkiddingbutseriously',
            f'\n',
            f'\n',
            f'The main fix for this update solves the slow-down issues while trying',
            f'to open up a project.',
            f'\n',
            f'\n',
            f'There also was some significant code improvements on both local and remote',
            f'servers to allow for new features coming in the near future!  Features such',
            f'as:',
            f'  - Locking projects if they are open by another user',
            f'  - Seeing who has a project open.',
            f'  - Adding labels to projects to start sorting between jams, active songs, ideas, etc.',
            f'  - And much more coming soon!',
            f'\n',
            f'\n',
            f'For more information, please refer to the repository commits.',
            f'\n',
            f'\n',
        ]
    )
    dialog.press_enter()

    # Remove 'env.py' in favor of .settings file
    File.delete("src/env.py")

    # Remove 'user' key from .settings
    Settings.delete_key("user")

    # 0 = there was a problem upgrading
    # 1 = do not restart core
    # 2 = restart core is necessary
    sys.exit(2)
