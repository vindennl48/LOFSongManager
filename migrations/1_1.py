# UPGRADE TO V1.1

import sys
from pathlib import Path
from src.settings.Settings import Settings
from src.helpers import pause
from src.helpers import clear_screen
from src.helpers import clear_folder

if __name__ == "__main__":
    output = [
        f'',
        f'',
        f'  :: Upgrading to V1.1!',
        f'',
        f'     This version includes the LOFSongManager "Core".',
        f'     You are no longer required to manually update this',
        f'     software.  It will automatically update on it\'s own',
        f'     the next time you run!',
        f'',
        f'',
        f'  :: Notice!',
        f'',
        f'     If you have not cleaned out the old "Pemi" project from',
        f'     the zoom call, you should do that now at the next prompt!',
        f'',
        f'     You will also be required to enter in your first name to',
        f'     allow LOFSongManager to prevent conflicts.',
        f'     If you have already done so in the previous update,',
        f'     you unfortunately have to do it one more time.  This will',
        f'     hopefully be the last!',
        f'',
        f'     Lastly, you will have to input the Slack WebHook Endpoints',
        f'     in order to integrate slack notifications.  You can access',
        f'     them in the following prompt, or in the "Sticky" document',
        f'     in the slack #lofsongmanager channel.',
        f'',
        f'',
    ]

    print( "\n".join(output) )
    pause()

    # Ask for new username and slackpoints
    Settings.set_user()
    Settings.set_slack_endpoints()

    # Clean out all previous project files
    clear_screen()
    print("\n\n  :: Would you like to remove all local projects and start fresh?\n\n")
    ans = input("(y/n): ")

    if ans == "y":
        print("\n\n  :: Are you sure? This can not be undone! \n\n")
        ans = input("(y/n): ")

        if ans == "y":
            clear_folder(Path("extracted_songs"))
            clear_folder(Path("compressed_songs"))


    # 0 = there was a problem upgrading
    # 1 = do not restart core
    # 2 = restart core is necessary
    sys.exit(1)
