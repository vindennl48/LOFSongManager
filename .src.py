import os
import shutil
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

def zip_file():
    if os.name == 'nt':
        os.system(f"tar -cf {destination} {file}")
    else:
        os.system(f"cd temp; zip -r .{destination} {file}")

def unzip_file(file, destination):
    if os.name == 'nt':
        os.system(f"tar -xf {file} -C {destination}")
    else:
        os.system(f"unzip {file} -d {destination}")

def ffmpeg(args, source, destination, codec=""):
    if os.name == 'nt':
        command = [
            args,
            source,
            codec,
            destination,
        ]
        cwd = Path.cwd()
        command_string = f'"{cwd}//ffmpeg//bin//ffmpeg.exe" {" ".join(command)}'
        os.system(command_string)
    else:
        command = [
            args,
            f'"{source}"',
            codec,
            f'"{destination}"',
        ]
        command_string = f'ffmpeg {" ".join(command)}'
        os.system(command_string)

def split_path(path):
    if os.name == 'nt':
        return path.split("\\")
    else:
        return path.split("/")

def mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass

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
        shutil.copyfile(src, dest)

def display_title(text):
    print(f"###############################")
    print(f"  LOF Studio One Song Manager  ")
    print(f"###############################")
    print(f":: {text} \n")

def list_options(options, no_back=False):
    for i, option in enumerate(options, start=1):
        if isinstance(option, list):
            print(f"   {i}) {option[0]}")
        else:
            print(f"   {i}) {option}")
    if not no_back:
        print("")
        print(f"   b) Back")
    print("")

    result = input(": ")

    if result == 'B' or result == 'b':
        main_menu()
    else:
        return result

def clear_temp():
    if os.name == 'nt':
        os.system("rd /s /q temp")
    else:
        os.system("rm -rf temp")
    mkdir("temp")

def pause():
    log("Press Enter to Continue..")
    input()


## MENU ITEMS
def extract():
    clear_screen()

    display_title("What project would you like?")

    # Get extracted project names and list them
    project_file_paths = glob("compressed_songs//*.zip")
    project_files      = [ split_path(x)[-1] for x in project_file_paths ]
    project_files      = [ x.replace(".zip","") for x in project_files ]
    ans = list_options(project_files)
    ans = int(ans)-1

    # Generate paths for all of our files and dirs
    project_file      = project_files[ans]
    project_file_path = project_file_paths[ans]
    extracted_path    = f"extracted_songs//{project_file}"
    temp_path         = f"temp//{project_file}"

    # Make sure the temp file is cleared and make temp dir
    clear_temp()

    # Unzip compressed project
    unzip_file(project_file_path, "temp")
    # os.system(f"unzip {project_file_path} -d ./temp")
    mkdir(f"{extracted_path}")
    for path in glob(f"{temp_path}//*"):
        name = split_path(path)[-1]
        if name != "Media":
            recursive_overwrite(path, f"{extracted_path}//{name}")

    # Convert all media files to wav from temp dir
    mkdir(f"{extracted_path}//Media")
    file_paths = glob(f"{temp_path}//Media//*.mp3")
    for file_path in file_paths:
        file_name = split_path(file_path)[-1].replace(".mp3","")
        if not os.path.exists(f"{extracted_path}//Media//{file_name}.wav"):
            ffmpeg("-i", f"{temp_path}//Media//{file_name}.mp3", f"{extracted_path}//Media//{file_name}.wav", "-c:a pcm_s24le")

    # Clean up after ourselves
    clear_temp()

    pause()

def compress():
    clear_screen()

    display_title("What project would you like?")

    # Get extracted project names and list them
    project_file_paths = glob("extracted_songs//*//")
    project_files      = [ split_path(x)[-2] for x in project_file_paths ]
    ans = list_options(project_files)
    ans = int(ans)-1

    # Generate paths for all of our files and dirs
    project_file      = project_files[ans]
    project_file_path = project_file_paths[ans][:-1]
    compressed_path   = f"compressed_songs//{project_file}.zip"
    temp_path         = f"temp//{project_file}"

    # Make sure the temp file is cleared and make temp dir
    clear_temp()

    # Extract existing compressed project first if exists
    if os.path.exists(f"{compressed_path}"):
        unzip_file(compressed_path, "temp")
        # os.system(f"unzip {compressed_path} -d ./temp")
    else:
        mkdir(f"{temp_path}")

    # Copy everything to temp except media dir
    if not os.path.exists(f"{temp_path}"):
        mkdir(f"{temp_path}")
    for path in glob(f"{project_file_path}//*"):
        name = split_path(path)[-1]
        if name != "Media":
            recursive_overwrite(path, f"{temp_path}//{name}")
            # os.system(f"cp -R {path} {temp_path}//.")

    # Convert all media files to mp3 in temp dir
    mkdir(f"{temp_path}//Media")
    file_paths = glob(f"{project_file_path}//Media//*.wav")
    for file_path in file_paths:
        file_name = split_path(file_path)[-1].replace(".wav","")
        if not os.path.exists(f"{temp_path}//Media//{file_name}.mp3"):
            ffmpeg("-i", f"{project_file_path}//Media//{file_name}.wav", f"{temp_path}//Media//{file_name}.mp3")
            # ffmpeg(f'-i "{project_file_path}//Media//{file_name}.wav" "{temp_path}//Media//{file_name}.mp3"')
            # os.system(f'ffmpeg -i "{project_file_path}/Media/{file_name}.wav" "{temp_path}/Media/{file_name}.mp3"')

    # os.system(f'for f in {project_file_path}/Media/*.wav; do ffmpeg -i "${{f}}" "${{f%.*}}.mp3"; done;')
    # os.system(f"mv {project_file_path}/Media/*.mp3 {temp_path}/Media/.")
    zip_file(project_file, compressed_path)
    # os.system(f"cd temp; zip -r .{compressed_path} {project_file}")

    # Clean up after ourselves
    clear_temp()

    log("Compression Complete!")
    pause()

def update_program():
    clear_screen()

    display_title("Updates")

    log("Checking for updates..")
    os.system("git pull")
    log("Update Complete!")
    input()

    exit_program()

def exit_program():
    log("Exiting Program..")
    exit()


## MAIN MENU
def main_menu():
    # Create default file structure if it doesnt exist
    mkdir("compressed_songs")
    mkdir("extracted_songs")
    mkdir("temp")
    mkdir("templates")

    clear_screen()
    display_title("What would you like to do?")

    menu_items = [
        ["Extract Project",  extract],
        ["Compress Project", compress],
        ["Update",           update_program],
        ["Exit",             exit_program],
    ]
    ans = list_options(menu_items, no_back=True)

    ans = int(ans)-1
    menu_items[ans][1]()

    main_menu()




## MAIN FUNCTION
if __name__ == '__main__':
    main_menu()
