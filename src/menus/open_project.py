import os
import time
from src.helpers import *
from src.settings.Settings import Settings
from src.slack.notify import Notify as Slack

def open_project(main_menu):
    clear_screen()
    display_title("What project would you like to open?")

    projects       = get_folders("extracted_songs")
    project        = projects[ list_options([ x.name for x in projects ], back=main_menu) ]
    local_version  = Path(f"{project.absolute()}/{project.name}.song")
    local_conflict = Path(f"{project.absolute()}/{project.name}_yourversion.song")

    # Push a notification to Slack
    Slack(f'{Slack.get_nice_username()} is working on {Slack.make_nice_project_name(project.name)}')

    if local_conflict.exists():
        print("")
        print(f':: A conflict exists in this project.')
        print("")
        print(f'   This occurs when changes to a local project fall behind')
        print(f'   the version that is in the cloud.')
        print("")
        print(f'   Would you like to:')
        print(f'     1) Open both?')
        print(f'     2) Open your last saved version?')
        print(f'     3) Open the most recent version from the cloud?')
        print("")
        print(f'     b) back')
        print("")
        ans = input(f'(1/2/3/b):')

        if ans == '1':
            log("Opening both projects..")
            open_SO_projects(local_version.absolute(), local_conflict.absolute())

        elif ans == '2':
            log("Opening your last saved version..")
            open_SO_projects(local_conflict.absolute())

        elif ans == '3':
            log("Opening the most recent version from the cloud")
            open_SO_projects(local_version.absolute())

        elif ans == 'b':
            return open_project(main_menu)

        else:
            log("Not a valid answer, please try again..")
            pause()
            return open_project(main_menu)
    else:
        log("Opening project")
        open_SO_projects(local_version.absolute())

    pause()
