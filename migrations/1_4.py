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
    dialog = Dialog(
        title = "Upgrading to V1.4!",
        body  = [
            f'A simple, innocent update that will switch SAM from Slack to Discord.',
            f'\n', f'\n',
            f'This update requires a manual change to the .settings file ',
            f'in this project. The old Slack endpoint keys and values ',
            f'need to be replaced with the new Discord endpoint keys and ',
            f'values. The new keys and values can be found in this file: ',
            f'\n', f'\n',
            f'   https://drive.google.com/file/d/1Q8KppHtX1ZW4ZJUIDa6fhQ-YxE44Hxkn/view?usp=sharing',
            f'\n',
            f'   Or, it is located in the Docs folder on the drive, "discord_webhook_endpoints.txt"',
            f'\n', f'\n',
            f'If you run into difficulty with this manual update, post a ',
            f'message in Discord and someone can assist.',
            f'\n', f'\n',
            f'For more information, please refer to the repository commits and/or the Discord channel.',
            f'\n', f'\n',
        ]
    )
    dialog.press_enter()

    Settings.set_discord_endpoints()

    # remove old keys
    if Settings.get_key("slack_endpoint_prod"):
        Settings.delete_key("slack_endpoint_prod")
    if Settings.get_key("slack_endpoint_dev"):
        Settings.delete_key("slack_endpoint_dev")
    if Settings.get_key("user"):
        Settings.delete_key("user")

    # 0 = there was a problem upgrading
    # 1 = do not restart core
    # 2 = restart core is necessary
    sys.exit(2)
