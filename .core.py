from pathlib import Path
from src.Discord import Discord
from src.Update import Update
from src.TERMGUI.Run import Run
from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog

def start_main_program():
    main = Path(".main.py")

    if main.exists():
        ans = Run.prg("python", f'"{main.absolute()}"', useSubprocess=True)

        if ans == 0:
            # There was an error
            Discord().post_log(Log.dump())
            raise Exception("\n\nThere was an error.. Contact your administrator.\n\n")

    else:
        Log(".main.py Does not exist!!", "warning")
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

        Discord().post_log(Log.dump())


## MAIN FUNCTION
if __name__ == "__main__":
    # only run the main program if update returns true
    if Update.run():
        start_main_program()
