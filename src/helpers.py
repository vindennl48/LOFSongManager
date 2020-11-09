import os
import subprocess
import re
import time
import json
import shutil
import filecmp
from glob import glob
from pathlib import Path
from src.env import VERSION
from src.dev import *

## HELPERS

# MAKE A NEW CLASS TO DEAL WITH STUDIO ONE
def open_project(file, wait=False):
    file = Path(file)
    prg  = "open"
    flag = "-W"

    if os.name == 'nt':
        prg  = "start"
        flag = "/wait"

    if not wait:
        flag = ""
    else:
        log("Waiting for Studio One to close..")
        print("\n\n      DO NOT CLOSE THIS WINDOW! \n\n")

    if not dev("NO_OPEN_STUDIO_ONE"):
        os.system(f'{prg} {flag} {file.absolute()}')
    else:
        log("Development Mode prevented Studio One from opening")

    if wait:
        log("Studio One has closed")


def open_SO_projects(*args):
    for i, project in enumerate(args, 1):
        project            = Path(project)
        local_version      = Path(f"{project.parent}/{project.stem}.song")
        local_version_temp = Path(f"{project.parent}/{project.stem}_temp.song")

        recursive_overwrite(local_version.absolute(), local_version_temp.absolute())

        if i == len(args):
            open_project(local_version_temp.absolute(), wait=True)
        else:
            open_project(local_version_temp.absolute())

            if len(args) > 1:
                log("Wait 10 sec for the next project to open..")
                time.sleep(10)

    for project in args:
        project            = Path(project)
        local_version      = Path(f"{project.parent}/{project.stem}.song")
        local_version_temp = Path(f"{project.parent}/{project.stem}_temp.song")

        recursive_overwrite(local_version_temp.absolute(), local_version.absolute())
        local_version_temp.unlink()
########################################
