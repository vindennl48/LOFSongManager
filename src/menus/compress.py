from glob import glob
from pathlib import Path
from src.helpers import *

def compress(main_menu):
    clear_screen()

    display_title("What project would you like?")

    # Get extracted project names and list them
    projects     = get_folders("extracted_songs")
    project      = projects[ list_options([ x.name for x in projects ], back=main_menu) ]
    temp_project = Path(f"temp/{project.name}")
    comp_project = Path(f"compressed_songs/{project.name}.lof")

    # Safety dialog to prevent a crap ton of unused audio files in the compressed file
    print("")
    ans = input("####> Have you removed all unused audio files from the Studio One pool? \n(y/n): ")
    if ans != 'y':
        log("Please clear out all unused audio files from the pool before compressing!")
        pause()
        exit()
    print("")

    # Make sure the temp file is cleared and make temp dir
    clear_temp()

    # Extract existing compressed project first if exists
    if comp_project.is_file():
        untar_file(comp_project, "temp")
    else:
        mkdir(temp_project)

    # Copy or convert files to temp dir
    for path in glob(f"{project}/*"):
        path = Path(path)

        if path.name == "Media":
            wav_to_mp3(f"{project}/Media", f"{temp_project}/Media")
        elif path.name == "Bounces":
            wav_to_mp3(f"{project}/Bounces", f"{temp_project}/Bounces")
        elif path.name != "Cache":
            recursive_overwrite(path.absolute(), f"{temp_project.absolute()}/{path.name}")
        else:
            pass
            # Cache folder gets re-generated when the project is opened by studio one

    tar_file(temp_project, comp_project)

    # Clean up after ourselves
    clear_temp()

    log("Compression Complete!")
    pause()
