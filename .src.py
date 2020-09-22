import os
from glob import glob


## HELPERS
def log(text):
    print("----> ", text)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

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
    os.system("rm -rf ./temp")
    os.system("mkdir -p ./temp")

def pause():
    log("Press Enter to Continue..")
    input()


## MENU ITEMS
def extract():
    clear_screen()

    display_title("What project would you like?")

    # Get extracted project names and list them
    project_file_paths = glob("./compressed_songs/*.zip")
    project_files      = [ x.split("/")[-1] for x in project_file_paths ]
    project_files      = [ x.replace(".zip","") for x in project_files ]
    ans = list_options(project_files)
    ans = int(ans)-1

    # Generate paths for all of our files and dirs
    project_file      = project_files[ans]
    project_file_path = project_file_paths[ans]
    extracted_path    = f"./extracted_songs/{project_file}"
    temp_path         = f"./temp/{project_file}"

    # Make sure the temp file is cleared and make temp dir
    clear_temp()

    # Unzip compressed project
    os.system(f"unzip {project_file_path} -d ./temp")
    os.system(f"mkdir -p {extracted_path}")
    for path in glob(f"{temp_path}/*"):
        name = path.split("/")[-1]
        if name != "Media":
            # print(f"cp -vR {path} {extracted_path}")
            os.system(f"cp -vR {path} {extracted_path}/.")

    # Convert all media files to wav from temp dir
    os.system(f"mkdir -p {extracted_path}/Media")
    file_paths = glob(f"{temp_path}/Media/*.mp3")
    for file_path in file_paths:
        file_name = file_path.split("/")[-1].replace(".mp3","")
        if not os.path.exists(f"{extracted_path}/Media/{file_name}.wav"):
            os.system(f'ffmpeg -i "{temp_path}/Media/{file_name}.mp3" -c:a pcm_s24le "{extracted_path}/Media/{file_name}.wav"')

    # Clean up after ourselves
    clear_temp()

    pause()

def compress():
    clear_screen()

    display_title("What project would you like?")

    # Get extracted project names and list them
    project_file_paths = glob("./extracted_songs/*/")
    project_files      = [ x.split("/")[-2] for x in project_file_paths ]
    ans = list_options(project_files)
    ans = int(ans)-1

    # Generate paths for all of our files and dirs
    project_file      = project_files[ans]
    project_file_path = project_file_paths[ans][:-1]
    compressed_path   = f"./compressed_songs/{project_file}.zip"
    temp_path         = f"./temp/{project_file}"

    # Make sure the temp file is cleared and make temp dir
    clear_temp()

    # Extract existing compressed project first if exists
    if os.path.exists(f"{compressed_path}"):
        os.system(f"unzip {compressed_path} -d ./temp")
    else:
        os.system(f"mkdir -p {temp_path}")

    # Copy everything to temp except media dir
    if not os.path.exists(f"{temp_path}"):
        os.system(f"mkdir -p {temp_path}")
    for path in glob(f"{project_file_path}/*"):
        name = path.split("/")[-1]
        if name != "Media":
            os.system(f"cp -R {path} {temp_path}/.")

    # Convert all media files to mp3 in temp dir
    os.system(f"mkdir -p {temp_path}/Media")
    file_paths = glob(f"{project_file_path}/Media/*.wav")
    for file_path in file_paths:
        file_name = file_path.split("/")[-1].replace(".wav","")
        if not os.path.exists(f"{temp_path}/Media/{file_name}.mp3"):
            os.system(f'ffmpeg -i "{project_file_path}/Media/{file_name}.wav" "{temp_path}/Media/{file_name}.mp3"')

    # os.system(f'for f in {project_file_path}/Media/*.wav; do ffmpeg -i "${{f}}" "${{f%.*}}.mp3"; done;')
    # os.system(f"mv {project_file_path}/Media/*.mp3 {temp_path}/Media/.")
    os.system(f"cd temp; zip -r .{compressed_path} {project_file}")

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
    os.system("mkdir -p compressed_songs extracted_songs temp templates")

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
