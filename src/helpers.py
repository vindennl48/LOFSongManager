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
def log(text):
    print("---->", text)

def pause():
    log("Press Enter to Continue..")
    input()

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def tar_file(file, destination):
    file        = Path(file)
    destination = Path(destination)
    cwd         = Path.cwd()

    log(f"Compressing {file.stem}")
    try:
        os.system(f'cd "{file.parent}" && tar -czf "{destination.absolute()}" "{file.name}" && cd "{cwd.absolute()}"')
    except Exception as e:
        log(f" Failed to compress {file.stem}..")
        print(e)
        exit()
    log(f"Compression of {file.stem} complete!")

def untar_file(file, destination):
    file        = Path(file)
    destination = Path(destination)

    log(f"Extracting {file.stem}")
    try:
        os.system(f"tar -xzf {file.absolute()} -C {destination.absolute()}")
    except Exception as e:
        log(f" Failed to extract {file.stem}..")
        print(e)
        exit()
    log(f"Extraction of {file.stem} complete!")

def ffmpeg(args, source, destination, codec=""):
    command        = []
    command_string = ""

    if os.name == 'nt':
        ffmpeg_path = Path("src/ffmpeg/bin/ffmpeg.exe")

        command = [
            f'"{ffmpeg_path.absolute()}"',
            f'{args}',
            f'"{source}"',
            f'{codec}',
            f'"{destination}"',
        ]

        command_string = " ".join(command)

        subprocess.call(command_string)

    else:
        command = [
            f'{args}',
            f'"{source}"',
            f'{codec}',
            f'"{destination}"',
        ]
        command_string = f'ffmpeg {" ".join(command)}'

        os.system(command_string)

def mp3_to_wav(directory, destination, dummy=None):
    # Directory is where the mp3's are stored
    # Destination is where you want the wav's to be saved
    directory   = Path(directory)
    destination = Path(destination)

    if not dummy:
        dummy = get_dummy_data(destination.absolute())

    mkdir(destination)
    for mp3 in glob(f"{directory}/*.mp3"):
        mp3 = Path(mp3)
        wav = Path(f"{destination}/{mp3.stem}.wav")
        if not wav.is_file():
            ffmpeg("-i", mp3.absolute(), wav.absolute(), "-c:a pcm_s24le")
        else:
            file_stem, num, ext = split_file_name(wav.name)
            if file_stem in dummy['max'] and num > dummy['max'][file_stem]:
                # We have an audio file conflict!
                # We are going to keep the newest version and rename
                # the other to *_old.wav
                print(f'')
                print(f':: Warning! Audio File Conflict Found!')
                print(f'')
                print(f'   Because the audio file "{wav.name}" exists in your local project')
                print(f'   as well as the cloud project you are trying to download.. We need')
                print(f'   to figure out which one to keep!')
                print(f'')
                print(f'   This software will take the current local version of "{wav.name}" and')
                print(f'   rename it to "{wav.stem}_old.wav".  Then copy the new audio file into')
                print(f'   the pool.  You will have to go into the project and figure out which')
                print(f'   audio file is the correct one!')
                print(f'')
                print(f'   Chances are you have accidentally recorded to the wrong track and this')
                print(f'   warning can be ignored.')
                print(f'')
                pause()
                recursive_overwrite(wav.absolute(), f'{wav.parent}/{wav.stem}_old.wav')
                wav.unlink()
                ffmpeg("-i", mp3.absolute(), wav.absolute(), "-c:a pcm_s24le")
            else:
                log(f'Keeping file "{wav}"')

def wav_to_mp3(directory, destination):
    # Directory is where the mp3's are stored
    # Destination is where you want the wav's to be saved
    directory   = Path(directory)
    destination = Path(destination)
    name        = get_username()
    name_ignore = False

    mkdir(destination)

    for wav in glob(f"{directory}/*.wav"):
        wav       = Path(wav)
        mp3       = Path(f"{destination}/{wav.stem}.mp3")
        is_old    = False
        wav_split = wav.stem.split('_')

        # Figure out if the file is *_old.wav
        if len(wav_split) > 1 and wav_split[-1] == "old":
            # If it is, we want to ignore the next section
            is_old = True

        if not mp3.is_file():
            if not name in wav.stem.lower() and not name_ignore and not is_old:
                print(f'')
                print(f':: Warning!')
                print(f'')
                print(f'   It appears that the file')
                print(f'')
                print(f'     "{wav.parent.absolute().name}/{wav.name}"')
                print(f'')
                print(f'   does not contain your name.. Are you sure you')
                print(f'   recorded on the correct track??  Doing this can')
                print(f'   cause serious version control issues!!')
                print(f'')
                print(f'   Since you have already removed unused audio files')
                print(f'   and selected the checkbox to delete them from the')
                print(f'   hard drive..  You should go back into your Studio')
                print(f'   One project, remove these clips from the time-   ')
                print(f'   line, remove unused audio files, then re-run the ')
                print(f'   upload.')
                print(f'')
                print(f'   If you are ABSOLUTELY SURE that this is in error,')
                print(f'   aka, uploading a project from band practice,')
                print(f'   then type "yes" at the prompt or yesall to ignore')
                print(f'   all other warnings in this upload.')
                print(f'')
                print(f'   If you want to exit now, type "no" at the prompt.')
                print(f'')

                ans = input("(yes/yesall/no): ")
                if ans == "no":
                    return 4
                elif ans == "yes":
                    pass
                elif ans == "yesall":
                    name_ignore = True
                else:
                    print(f'Not a valid response.. Please try again!')
                    wav_to_mp3(directory, destination)

            ffmpeg("-i", wav.absolute(), mp3.absolute())
        else:
            log(f'Keeping file "{mp3}"')

def mkdir(path):
    path = Path(path)

    if path.is_file():
        log(f'Error: "{path.name}" is already a file!')
        log( "       Exiting Program..")
        exit()
    elif path.is_dir():
        log(f'Warning: Directory "{path.name}" already exists!')
        return False
    else:
        os.makedirs(path.absolute())
        log(f'Created directory "{path.name}"')
        return True

def recursive_overwrite(src, dest, ignore=None):
    # taken from: https://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f),
                                    os.path.join(dest, f),
                                    ignore)
    else:
        src  = Path(src)
        dest = Path(dest)

        if dest.exists():
            if not filecmp.cmp(src.absolute(), dest.absolute(), shallow=False):
                log(f'Overwriting file "{src.name}"')
            else:
                log(f'Keeping file "{src.name}"')
                return 0
        else:
            log(f'Copying new file "{src.name}"')

        shutil.copyfile(src, dest)
def display_title(text):
    if dev("DEVELOPMENT"):
        print(f"::      DEVELOPMENT MODE     ::")

    print(f"###############################")
    print(f"  LOF Studio One Song Manager  ")
    print(f"            V{VERSION}         ")
    print(f"###############################")
    print(f":: {text} \n")

def list_options(options, back=False):
    for i, option in enumerate(options, start=1):
        if isinstance(option, list):
            print(f"   {i}) {option[0]}")
        else:
            print(f"   {i}) {option}")
    if back:
        print("")
        print(f"   b) Back")
    print("")

    result = input(": ")

    if back and (result == 'B' or result == 'b'):
        back()
    elif result.isnumeric() and int(result) <= len(options):
        return (int(result) - 1)
    else:
        log("Invalid response, please try again..")
        pause()
        return list_options(options, back)

def clear_folder(path):
    path = Path(path)
    log(f"Clearing out '{path.name}' directory..")
    if path.exists():
        shutil.rmtree(path.absolute())
    mkdir(path.absolute())
    log(f"'{path.name}' directory cleared!")

def clear_temp():
    if not dev("NO_CLEAR_TEMP"):
        log("Clearing out temp directory..")
        shutil.rmtree("temp")
        mkdir("temp")
    else:
        log("Development Mode prevented clear_temp function")
    log("Temp directory cleared!")

def git_update():
    if os.name == 'nt':
        git = Path("src/PortableGit/bin/git")
        os.system(f'"{git.absolute()}" pull --rebase')
    else:
        os.system("git pull --rebase")

def get_folders(directory):
    directory = Path(directory)
    folders = glob(f"{directory.absolute()}/*/")
    folders = [ Path(x) for x in folders ]
    return folders

def get_files(directory, extension):
    directory = Path(directory)
    files = glob(f"{directory.absolute()}/*.{extension}")
    files = [ Path(x) for x in files ]
    return files

def split_file_name(file):
    # This splits a filename 'Mitch(23).wav' into
    # [ "Mitch", 23 ] or 'Mitch(REC)(26).wav' into
    # [ "Mitch(REC)", 26 ]
    file, ext  = file.split(".")
    file_array = file.split("(")
    num        = re.findall(r"(\d+)\)", file_array[-1])
    num        = int(num[0]) if len(num) > 0 else 0
    file_stem  = ""

    if num > 0:
        file_array.pop()
    file_stem = "(".join(file_array)

    return [ file_stem, num, ext ]

def get_dummy_data(project_dir):
    log("Getting dummy data")
    project_dir = Path(project_dir)
    dummy       = project_dir / "dummy.json"
    db          = {'max': {}, 'dummy': []}

    if dummy.parent.exists():
        # if the db store doesnt exist
        if not dummy.exists():
            log("Creating dummy.json file..")
            with open(dummy.absolute(), 'w') as f:
                json.dump(db, f)

        # get db store from json
        with open(dummy.absolute()) as f:
            db = json.load(f)

    return db

def create_dummy_files(project_dir):
    log("Creating dummy .wav files..")
    project_dir = Path(project_dir)
    project_dir = project_dir / "Media"
    dummy       = project_dir / "dummy.json"
    db          = {'max': {}, 'dummy': []}

    unprocessed_files = glob(f"{project_dir.absolute()}/*.wav")
    unprocessed_files = [ Path(x).name for x in unprocessed_files ]

    # if the db store doesnt exist
    if not dummy.exists():
        log("Creating dummy.json file..")
        with open(dummy.absolute(), 'w') as f:
            json.dump(db, f)

    # get db store from json
    with open(dummy.absolute()) as f:
        db = json.load(f)

    for file in unprocessed_files:
        file_stem, num, ext = split_file_name(file)

        if not file_stem in db['max']:
            db['max'][file_stem] = num
        else:
            if num > db['max'][file_stem]:
                db['max'][file_stem] = num

    for file_stem in db['max']:
        num = db['max'][file_stem]

        for i in range(num):
            if i == 0:
                path = Path(f"{project_dir}/{file_stem}.{ext}")
            else:
                path = Path(f"{project_dir}/{file_stem}({i}).{ext}")

            if not path.exists():
                path.touch()
                db['dummy'].append(path.name)

    with open(dummy.absolute(), 'w') as f:
        json.dump(db, f)

    log("Created dummy files!")

def remove_dummy_files(project_dir_raw):
    log("Removing dummy .wav files..")
    project_dir = Path(project_dir_raw)
    project_dir = project_dir / "Media"
    dummy       = project_dir / "dummy.json"
    db          = {}

    if not dummy.exists():
        create_dummy_files(project_dir_raw)

    # get db store from json
    with open(dummy.absolute()) as f:
        db = json.load(f)

    for file in db['dummy']:
        file = Path(f"{project_dir}/{file}")
        if file.stat().st_size == 0:
            file.unlink()

    # clean out dummy file list
    db['dummy'] = []

    # save new dummy.json
    with open(dummy.absolute(), 'w') as f:
        json.dump(db, f)

    log("Removed dummy files!")

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

def create_settings():
    # if settings dont exist
    settings_file = Path('.settings')
    settings      = {}

    if settings_file.exists():
        with open(settings_file.absolute()) as f:
            settings = json.load(f)

        if not "version" in settings or settings['version'] != VERSION:
            settings_file.unlink()

    if not settings_file.exists():
        print(':: Welcome!')
        print('')
        print('   Since this is your first time using this software, we')
        print('   need to know your name to get things working smoothly!')
        print('')
        print('   What is your first name?')
        print('')

        name = input("Name: ").lower()

        print('\n   Thanks!!\n')

        pause()

        settings['user']    = name
        settings['version'] = VERSION

        with open(settings_file.absolute(), 'w') as f:
            json.dump(settings, f)

def get_username():
    settings_file = Path('.settings')
    settings      = {}

    if not settings_file.exists():
        create_settings()

    with open(settings_file.absolute()) as f:
        settings = json.load(f)

    return settings['user']

def get_nice_username():
    return get_username().capitalize()
