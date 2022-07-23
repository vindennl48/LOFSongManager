# UPGRADE TO V1.4

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
            title = "Upgrading to V1.4!",
            body  = [
                f'A simple, innocent update that will switch SAM from Slack to Discord.',
                f'\n', f'\n',
                f'For more information, please refer to the repository commits and/or the Discord channel.',
                f'\n', f'\n',
            ]
        )
        dialog.press_enter()

        Log("A restart is needed to update the core!","notice")
        Log("Please ignore the following error message and restart the program.","sub")
        Log.press_enter()
        # 0 = there was a problem upgrading
        # 1 = do not restart core
        # 2 = restart core is necessary
        sys.exit(0)

    dialog = Dialog(
        title = "Upgrading to V1.4!",
        body  = [
            f'Hang tight...',
            f'\n', f'\n',
        ]
    )
    dialog.press_enter()

    # Now that we have updated the core, we can continue with the rest of the update!
    Settings.delete_key("update_git")

    # Set up the new endpoints for Discord webhooks
    Discord.reset_discord_endpoints()

    # 0 = there was a problem upgrading
    # 1 = do not restart core
    # 2 = restart core is necessary
    sys.exit(2)

