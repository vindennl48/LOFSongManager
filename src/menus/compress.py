from glob import glob
from pathlib import Path
from src.helpers import *

def compress(main_menu):
    clear_screen()

    display_title("What project would you like to compress?")

    # Get extracted project names and list them
    projects     = get_folders("extracted_songs")
    project      = projects[ list_options([ x.name for x in projects ], back=main_menu) ]
    temp_project = Path(f"temp/{project.name}")
    comp_project = Path(f"compressed_songs/{project.name}.lof")

    local_original   = Path(f"{project}/{project.stem}_original.song")
    local_conflict   = Path(f"{project}/{project.stem}_yourversion.song")
    local_version    = Path(f"{project}/{project.stem}.song")
    download_version = Path(f"{temp_project}/{project.stem}.song")

    # Make sure the temp file is cleared and make temp dir
    clear_temp()

    # Extract existing compressed project first if exists
    if comp_project.is_file():
        untar_file(comp_project, "temp")
    else:
        mkdir(temp_project)

    # If the compressed version is the same as the extracted version
    if local_version.exists() and download_version.exists() \
            and filecmp.cmp(local_version.absolute(), download_version.absolute()):
        print("")
        print(f':: You already have the most up-to-date')
        print(f'   compressed project for "{project.stem}"!')
        print("")
        print(f'   Continuing is not advisable!')
        print("")
        print("   Continue anyway?")
        if input("   (y/n): ") != 'y':
            return 0

    # Check to make sure there are no prior conflicts
    if local_conflict.exists():
        log("Warning: You still have existing conflicts!!")
        print("")
        print(f':: Project file "{local_conflict}" still exists.')
        print(f'   This gets created when there are conflicts between your local project')
        print(f'   and an updated project downloaded from the drive.  If these conflicts')
        print(f'   do not get resolved before you download yet another version, you will')
        print(f'   lose all of your local changes!')
        print("")
        print(f'   If you have ALREADY resolved these conflicts but have not yet deleted')
        print(f'   the "{local_conflict}" file, then type "yes".')
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

    # Copy or convert files to temp dir
    for path in glob(f"{project}/*"):
        path = Path(path)

        # catch all *.song files but ignore all but the main *.song file
        if path.suffix == ".song":
            # We only want to compress the *.song file
            if path.name == local_version.name:
                recursive_overwrite(local_version.absolute(), download_version.absolute())
                recursive_overwrite(local_version.absolute(), local_original.absolute())
        elif path.name == "Media":
            wav_to_mp3(f"{project}/Media", f"{temp_project}/Media")
        elif path.name == "Bounces":
            wav_to_mp3(f"{project}/Bounces", f"{temp_project}/Bounces")
        elif path.name != "Cache" and path.suffix != ".autosave":
            recursive_overwrite(path.absolute(), f"{temp_project.absolute()}/{path.name}")
        else:
            pass
            # Cache folder gets re-generated when the project is opened by studio one
            # We don't need to compress the autosave files.
            # We also don't need to save the autosave history but we can do that later,
            #  The filesize isnt that expensive.

    tar_file(temp_project, comp_project)

    # Clean up after ourselves
    clear_temp()

    log("Compression Complete!")
    pause()
