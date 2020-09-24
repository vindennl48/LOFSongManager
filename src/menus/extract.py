import filecmp
from glob import glob
from pathlib import Path
from src.helpers import *

def extract(main_menu):
    clear_screen()

    display_title("What project would you like?")

    # Get extracted project names and list them
    comp_projects    = get_files("compressed_songs", "lof")
    comp_project     = comp_projects[ list_options([ x.stem for x in comp_projects ], back=main_menu) ]
    temp_project     = Path(f"temp/{comp_project.stem}")
    project          = Path(f"extracted_songs/{comp_project.stem}")
    local_original   = Path(f"{project}/{project.stem}_original.song")
    local_conflict   = Path(f"{project}/{project.stem}_yourversion.song")
    local_version    = Path(f"{project}/{project.stem}.song")
    download_version = Path(f"{temp_project}/{project.stem}.song")

    # Make sure the temp file is cleared and make temp dir
    clear_temp()

    # Untar compressed project to temp
    untar_file(comp_project, "temp")

    # If the compressed version is the same as the extracted version
    if local_original.exists() and download_version.exists() \
            and filecmp.cmp(local_original.absolute(), download_version.absolute()):
        print("")
        print(f':: You already have the most up-to-date project')
        print(f'   extracted for "{project.stem}"!')
        print("")
        print(f'   Continuing is not advisable!')
        print("")
        print("   Continue anyway?")
        if input("   (y/n): ") != 'y':
            pause()
            return 0

    # Check to make sure there are no prior conflicts
    if local_conflict.exists():
        log("Warning: You still have existing conflicts!!")
        print("")
        print(f':: Project file "{project}/{project.stem}_yourversion.song" still exists.')
        print(f'   This gets created when there are conflicts between your local project')
        print(f'   and an updated project downloaded from the drive.  If these conflicts')
        print(f'   do not get resolved before you download yet another version, you will')
        print(f'   lose all of your local changes!')
        print("")
        print(f'   If you have ALREADY resolved these conflicts but have not yet deleted')
        print(f'   "the {project}/{project.stem}_yourversion.song" file, then type "yes".')
        print("")
        print(f'   If you have NOT yet resolved these conflicts, then type "no"')
        print("")
        if input("   (yes/no): ") == "yes":
            print(":: Are you definitely sure you want to erase your conflict file?")
            if input("   (yes/no): ") != "yes":
                log("Exiting...")
                pause()
                exit()
        else:
            log("Exiting...")
            pause()
            exit()

        local_conflict.unlink()

    # Make dir for new song if it doesnt exist
    new_project = mkdir(project)

    # Copy or convert files to extracted_songs dir
    for path in glob(f"{temp_project}/*"):
        path = Path(path)

        if path.name == f"{project.stem}.song":
            if local_original.exists() and local_version.exists():
                # If you made changes to the studio one file, this wont overwrite your progress.  We will
                #  save it as a different version so you can go back and compare the new downloaded 
                #  version with your version.
                if not filecmp.cmp(local_version.absolute(), local_original.absolute(), shallow=False):
                    print("")
                    print(f':: Local changes to this project have been detected!')
                    print("")
                    print(f'   When local changes are detected, this software will generate a secondary conflict version')
                    print(f'   called: ')
                    print("")
                    print(f'       "{local_conflict}"')
                    print("")
                    print(f'   You must open both projects and copy your changes from ')
                    print("")
                    print(f'       "{local_conflict}" TO "{local_version}".')
                    print("")
                    print(f'   "{local_version.name}" is the only one that gets uploaded.')
                    print("")
                    print(f'   Unfortunately, it is not possible to handle these conflicts programatically at this time.')
                    print("")
                    pause()
                    recursive_overwrite(local_version.absolute(), local_conflict.absolute())
            elif not local_version.exists() and not new_project:
                log(f'There is a problem.. No project file "{local_version}" exists..')
                pause()
                exit()

            recursive_overwrite(download_version.absolute(), f"{project.absolute()}/{download_version.name}")
            recursive_overwrite(download_version.absolute(), f"{project.absolute()}/{download_version.stem}_original.song")

        elif path.name == "Media":
            mp3_to_wav(f"{temp_project}/Media", f"{project}/Media")
        elif path.name == "Bounces":
            mp3_to_wav(f"{temp_project}/Bounces", f"{project}/Bounces")
        else:
            recursive_overwrite(path.absolute(), f"{project.absolute()}/{path.name}")

    # Clean up after ourselves
    clear_temp()

    pause()
