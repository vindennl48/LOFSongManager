from pathlib import Path
from src.update.Update import Update
from src.run.Run import Run
from src.helpers import pause

def start_main_program():
    main = Path("src/menus/main_menu.py")

    if main.exists():
        Run.prg("python", f'"{main.absolute()}"')
    else:
        raise Exception(f'"{main.absolute()}" doesnt exist!.. Something went terribly wrong..')


## MAIN FUNCTION
if __name__ == "__main__":
    # only run the main program if update returns true
    if Update.run():
        start_main_program()
