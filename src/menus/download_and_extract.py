import filecmp
from glob import glob
from pathlib import Path
from src.helpers import *
from src.hashing import *
from src.Drive import Drive
from src.env import LOFSM_DIR_HASH

def download_and_extract(main_menu):
    print("")
    log("loading projects from cloud..")

    # Get extracted project names and list them
    drive          = Drive()
    drive_projects = drive.ls(search=LOFSM_DIR_HASH)

    clear_screen()
    display_title("What project would you like to download and extract?")
    drive_projects = [ x for x in drive_projects if x['mimeType'] == Drive.mimeType['zip'] ]
    drive_project = drive_projects[ list_options([ x['name'] for x in drive_projects ], back=main_menu) ]

    comp_project     = Path(f"compressed_songs/{drive_project['name']}")
    temp_project     = Path(f"temp/{comp_project.stem}")
    project          = Path(f"extracted_songs/{comp_project.stem}")
    local_original   = Path(f"{project}/{project.stem}_original.song")
    local_conflict   = Path(f"{project}/{project.stem}_yourversion.song")
    local_version    = Path(f"{project}/{project.stem}.song")
    download_version = Path(f"{temp_project}/{project.stem}.song")

    # check hashes
    if not compare_hash(drive, comp_project.name):
        # We need to download the newest version
        log("Downloading new version")
        if not drive.download(drive_project['id'], comp_project.absolute()):
            raise Exception('\n\n## Check your internet connection and try again! ##\n## Error when downloading project ##')
        else:
            set_local_hash_from_remote(drive, comp_project.name)

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
        print(f'   If you have any saved changes in this project, it will be converted')
        print(f'   into a conflict file for you to re-merge again.  Only do this if you')
        print(f'   wish to start fresh with the latest cloud project!')
        print("")
        print("   Continue?")
        if input("   (y/n): ") != 'y':
            return 0

    # Check to make sure there are no prior conflicts
    if local_conflict.exists():
        log("Warning: You still have existing conflicts!!")
        print("")
        print(f':: Project file "{local_conflict}" still exists.')
        print(f'   This gets created when there are conflicts between your local project')
        print(f'   and an updated project downloaded from the cloud.  If these conflicts')
        print(f'   do not get resolved before you download yet another version, you will')
        print(f'   lose all of your local changes!')
        print("")
        print(f'   Note: Your audio files will not be erased from the pool.')
        print(f'         You can ignore the message before this.')
        print("")
        print(f'   If you have ALREADY resolved these conflicts, then type "yes"')
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

    # if there are any new changes to this project, return True
    has_conflicts = False
    if not new_project:
        has_conflicts = not filecmp.cmp(local_version.absolute(), local_original.absolute(), shallow=False)

    # Copy or convert files to extracted_songs dir
    for path in glob(f"{temp_project}/*"):
        path = Path(path)

        # catch all *.song files but ignore all but the main *.song file
        if path.suffix == ".song":
            if path.name == local_version.name:
                if local_original.exists() and local_version.exists():
                    # If you made changes to the studio one file, this wont overwrite your progress.  We will
                    #  save it as a different version so you can go back and compare the new downloaded 
                    #  version with your version.
                    if has_conflicts:
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
                        pause()
                        recursive_overwrite(local_version.absolute(), local_conflict.absolute())
                elif not local_version.exists() and not new_project:
                    log(f'There is a problem.. No project file "{local_version}" exists..')
                    pause()
                    exit()

                recursive_overwrite(download_version.absolute(), f"{project.absolute()}/{download_version.name}")
                recursive_overwrite(download_version.absolute(), f"{project.absolute()}/{download_version.stem}_original.song")
        elif path.name == "Media":
            if not has_conflicts:
                # save dummy.json
                dummy = Path(f"{project}/Media/dummy.json")
                db    = {}
                if dummy.exists():
                    with open(dummy.absolute(), 'r') as f:
                        db = json.load(f)

                # remove audio files in media folder
                clear_folder(f"{project}/Media")

                # if the db store doesnt exist
                if dummy.exists():
                    with open(dummy.absolute(), 'w') as f:
                        json.dump(db, f)

            mp3_to_wav(f"{temp_project}/Media", f"{project}/Media")
        elif path.name == "Bounces":
            if not has_conflicts:
                # remove audio files in bounces folder
                clear_folder(f"{project}/Bounces")

            mp3_to_wav(f"{temp_project}/Bounces", f"{project}/Bounces")
        else:
            recursive_overwrite(path.absolute(), f"{project.absolute()}/{path.name}")

    # Clean up after ourselves
    clear_temp()

    # Create dummy media files
    create_dummy_files(project)

    pause()
