import sys
from src.Slack import Slack
from src.Update import Update
from src.Settings import Settings
from src.TERMGUI.Log import Log
from src.FileManagement.Folder import Folder
from src.menus.menu_main import menu_main

# MAIN FUNCTION
if __name__ == '__main__':

    # Create file structure if it doesn't exist
    Folder.create("compressed_songs")
    Folder.create("extracted_songs")
    Folder.create("temp")
    Folder.create("templates")

    # Create settings file if it doesn't exist
    Settings.create()

    # Check version
    Update.check_version()

    # Start main menu
    try:
        menu_main()
    except Exception as e:
        Log(e, "warning")

        # 0 = there was a problem
        # 1 = exit gracefully
        sys.exit(0)
