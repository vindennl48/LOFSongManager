import os
from src.TERMGUI.Log import Log

class Term:
    def clear():
        command = "clear"

        if os.name == "nt":
            command = "cls"

        os.system(command)

        # Log.save_to_file("\n  ## *ClearScreen* ##\n")

