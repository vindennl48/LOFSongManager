from pathlib import Path
from src.Update import Update
from src.TERMGUI.Run import Run
from src.TERMGUI.Dialog import Dialog

def start_main_program():
    main = Path(".main.py")

    if main.exists():
        ans = Run.prg("python", f'"{main.absolute()}"', useSubprocess=True)

        if ans == 0:
            # There was an error
            pass

    else:
        Dialog(
            title = "Fatal Error!",
            body  = [
                f'"{main.absolute()}" doesnt exist!',
                f'\n',
                f'\n',
                f'Something went terribly wrong.. Contact your',
                f'administrator.',
                f'\n',
                f'\n',
            ],
            clear = False
        ).press_enter()


## MAIN FUNCTION
if __name__ == "__main__":
    # only run the main program if update returns true
    if Update.run():
        start_main_program()
