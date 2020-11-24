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
        title = "Upgrading to V1.2!",
        body  = [
            f'This version updates a LOT of the under-the-hood code to',
            f'help streamline the coding process.',
            f'\n',
            f'\n',
            f'The main menu has changed!  Now, the "Open" option takes care',
            f'of all of the upload and download tasks as well as conflicts.',
            f'In the "Open" screen, there will be labels on the right side',
            f'of the projects to tell you what the status is.',
            f'\n',
            f'\n',
            f'    1) Pemi          - Update',       f'\n',
            f'    2) Slough        - Dirty',        f'\n',
            f'    3) Trenches      - Not Uploaded', f'\n',
            f'    4) HelloGoodbye  - New',
            f'\n',
            f'\n',
            f'Update: There is a new project on the drive that will be downloaded',
            f'the next time you open.',
            f'\n',
            f'\n',
            f'Dirty: You have changes that have not been uploaded to the cloud yet.',
            f'\n',
            f'\n',
            f'Update (Conflict!): There is a new project on the drive but you also',
            f'have non-uploaded changes.. This will create a conflict file that you',
            f'will have to resolve.',
            f'\n',
            f'\n',
            f'Not Uploaded: A project you created that does not exist yet on the',
            f'drive',
            f'\n',
            f'\n',
            f'New: A project that exists on the drive but has not yet been downloaded.',
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
            f'this update has completed, the software should shut down on its',
            f'own.  If it does not, please restart the software.',
            f'\n',
            f'\n',
            f'For more information, please refer to the repository commits.',
            f'\n',
            f'\n',
        ]
    )
    dialog.press_enter()

    File.delete("development.py")
    File.delete("compressed_songs/db.json")

    # Change 'user' key to 'username' in settings
    Settings.set_key( "username", Settings.get_key("user") )

    # just to make sure we have the right ones
    Settings.reset_slack_endpoints()

    # 0 = there was a problem upgrading
    # 1 = do not restart core
    # 2 = restart core is necessary
    sys.exit(2)
