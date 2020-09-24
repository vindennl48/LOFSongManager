from glob import glob
from pathlib import Path
from src.helpers import *

def extract(main_menu):
    clear_screen()

    display_title("What project would you like?")

    # Get extracted project names and list them
    comp_projects = get_files("compressed_songs", "lof")
    comp_project  = comp_projects[ list_options([ x.stem for x in comp_projects ], back=main_menu) ]
    temp_project  = Path(f"temp/{comp_project.stem}")
    project       = Path(f"extracted_songs/{comp_project.stem}")

    # Make sure the temp file is cleared and make temp dir
    clear_temp()

    # Untar compressed project to temp
    untar_file(comp_project, "temp")

    # Make dir for new song if it doesnt exist
    mkdir(project)

    # Copy or convert files to extracted_songs dir
    for path in glob(f"{temp_project}/*"):
        path = Path(path)

        # if path.suffix == ".song":
            # print(path.absolute())
        if path.name == "Media":
            mp3_to_wav(f"{temp_project}/Media", f"{project}/Media")
        elif path.name == "Bounces":
            mp3_to_wav(f"{temp_project}/Bounces", f"{project}/Bounces")
        else:
            recursive_overwrite(path.absolute(), f"{project.absolute()}/{path.name}")

    # Clean up after ourselves
    clear_temp()

    pause()
