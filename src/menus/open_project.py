import os
import time
from src.helpers import *

def open_project(main_menu):
    clear_screen()
    display_title("What project would you like to open?")

    projects            = get_folders("extracted_songs")
    project             = projects[ list_options([ x.name for x in projects ], back=main_menu) ]
    local_version       = Path(f"extracted_songs/{project.name}/{project.name}.song")
    local_conflict      = Path(f"extracted_songs/{project.name}/{project.name}_yourversion.song")
    local_version_temp  = Path(f"extracted_songs/{project.name}/{project.name}_temp.song")
    local_conflict_temp = Path(f"extracted_songs/{project.name}/{project.name}_yourversion_temp.song")

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

            recursive_overwrite(local_version.absolute(), local_version_temp.absolute())
            os.system(f'open {local_version_temp.absolute()}')

            time.sleep(2)

            recursive_overwrite(local_conflict.absolute(), local_conflict_temp.absolute())
            os.system(f'open -W {local_conflict_temp.absolute()}')

            recursive_overwrite(local_version_temp.absolute(), local_version.absolute())
            recursive_overwrite(local_conflict_temp.absolute(), local_conflict.absolute())
            local_version_temp.unlink()
            local_conflict_temp.unlink()

        elif ans == '2':
            log("Opening your last saved version..")

            recursive_overwrite(local_conflict.absolute(), local_conflict_temp.absolute())
            os.system(f'open -W {local_conflict_temp.absolute()}')
            recursive_overwrite(local_conflict_temp.absolute(), local_conflict.absolute())
            local_conflict_temp.unlink()

        elif ans == '3':
            log("Opening the most recent version from the cloud")

            recursive_overwrite(local_version.absolute(), local_version_temp.absolute())
            os.system(f'open -W {local_version_temp.absolute()}')
            recursive_overwrite(local_version_temp.absolute(), local_version.absolute())
            local_version_temp.unlink()

        elif ans == 'b':
            return open_project(main_menu)

        else:
            log("Not a valid answer, please try again..")
            pause()
            return open_project(main_menu)
    else:
        log("Opening project")

        recursive_overwrite(local_version.absolute(), local_version_temp.absolute())
        os.system(f'open -W {local_version_temp.absolute()}')
        recursive_overwrite(local_version_temp.absolute(), local_version.absolute())
        local_version_temp.unlink()

    pause()
