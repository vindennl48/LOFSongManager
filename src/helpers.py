import os
import shutil
import filecmp
import hashlib
from glob import glob
from pathlib import Path

## HELPERS
def log(text):
    print("----> ", text)

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
        command = [
            args,
            source,
            codec,
            destination,
        ]
        ffmpeg_path = Path("src/ffmpeg/bin/ffmpeg.exe")
        command_string = f'"{ffmpeg_path.absolute()}" {" ".join(command)}'
    else:
        command = [
            args,
            f'"{source}"',
            codec,
            f'"{destination}"',
        ]
        command_string = f'ffmpeg {" ".join(command)}'

    os.system(command_string)

def mp3_to_wav(directory, destination):
    # Directory is where the mp3's are stored
    # Destination is where you want the wav's to be saved
    directory   = Path(directory)
    destination = Path(destination)

    mkdir(destination)
    for mp3 in glob(f"{directory}/*.mp3"):
        mp3 = Path(mp3)
        wav = Path(f"{destination}/{mp3.stem}.wav")
        if not wav.is_file():
            ffmpeg("-i", mp3.absolute(), wav.absolute(), "-c:a pcm_s24le")
        else:
            log(f'Keeping file "{wav.name}"')

def wav_to_mp3(directory, destination):
    # Directory is where the mp3's are stored
    # Destination is where you want the wav's to be saved
    directory   = Path(directory)
    destination = Path(destination)

    mkdir(destination)
    for wav in glob(f"{directory}/*.wav"):
        wav = Path(wav)
        mp3 = Path(f"{destination}/{wav.stem}.mp3")
        if not mp3.is_file():
            ffmpeg("-i", wav.absolute(), mp3.absolute())
        else:
            log(f'Keeping file "{mp3.name}"')

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
    print(f"###############################")
    print(f"  LOF Studio One Song Manager  ")
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

def clear_temp():
    log("Clearing out temp directory..")
    shutil.rmtree("temp")
    mkdir("temp")
    log("Temp directory cleared!")

def git_update():
    if os.name == 'nt':
        git = Path("src/PortableGit/bin/git")
        os.system(f'"{git.absolute()}" pull --rebase')
    else:
        os.system("git pull --rebase")

def pause():
    log("Press Enter to Continue..")
    input()

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

def hash_file(file):
    file       = Path(file)
    BLOCK_SIZE = 1024*1024
    result     = hashlib.sha256()

    with open(file.absolute(), 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            result.update(fb)
            fb = f.read(BLOCK_SIZE)

    return result.hexdigest()
