# UPGRADE TO V1.1

# this is required to access 'src' modules
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir  = os.path.dirname(currentdir)
sys.path.append(parentdir)
##########################################

from src.File import File
from src.TERMGUI.Dialog import Dialog

if __name__ == "__main__":
    dialog = Dialog(
        title = "Upgrading to V1.2!",
        body  = [
            f'This version updates a lot of the under-the-hood code to',
            f'help streamline the coding process.',
            f'\n',
            f'\n',
            f'For Developers:',
            f'\n',
            f'  This update removes the "development.py" file and replaces it',
            f'with a ".dev" json file instead.  This provides easier access',
            f'to development variables and a cleaner and more streamlined',
            f'approach to development.',
            f'\n',
            f'\n',
            f'  In addition, most of the functional code that existed in v1.1',
            f'has been converted to OOP.  This provides an easier environment',
            f'for moving forward as well as being easier to read and understand.',
            f'\n',
            f'\n',
            f'Note:',
            f'\n',
            f'  This update requires a full restart of LOFSongManager.  When',
            f'this update has completed, the software will shut down on its',
            f'own.',
            f'\n',
            f'\n',
        ]
    )

    File.delete("development.py")

    # 0 = there was a problem upgrading
    # 1 = do not restart core
    # 2 = restart core is necessary
    sys.exit(2)
