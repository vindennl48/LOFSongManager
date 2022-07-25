import textwrap, os
from datetime import datetime
from pathlib import Path
from src.FileManagement.FileEdit import FileEdit

class Log:

    filepath = ".log"
    line     = 0

    def __init__(self, text, leader="arrow", end=">", quiet=False):
        Log.out(text, leader, end, quiet)

    def out(text, leader, end, quiet):
        if leader == "warning":
            leader = "####"
            end    = " "

        elif leader == "notice":
            leader = "  =="

        elif leader == "alert":
            leader = "  ::"
            end    = " "

        elif leader == "sub":
            leader = "    "
            end    = " "

        elif leader == 6 or leader == "arrow":
            leader = "----"

        elif leader == None:
            leader = ""
            end    = ""

        output = f'{leader}{end} {text}'
        Log.save_to_file(output)

        if not quiet:
            print(output)

    def warning(text):
        output = f'\n  ## {text} ## \n'
        Log.save_to_file(output)
        print(output)

    def press_enter():
        Log.out(
            "Press Enter to Continue..",
            leader = "  > ",
            end    = ">",
            quiet  = False
        )
        input()

    def save_to_file(text):
        if Log.line == 0:
            FileEdit.delete(Log.filepath)

            FileEdit.append(
                Log.filepath,
                "\n".join([
                    "##############################",
                    str(datetime.now()).center(30),
                    "##############################",
                    "",
                ])
            )

        FileEdit.append(Log.filepath, f'{Log.line}: {text}')

        Log.line += 1

    def dump():
        filepath = Path(Log.filepath)
        result   = None

        if filepath.exists():
            with open(filepath.absolute()) as f:
                result = f.read()

        return result
