from glob import glob
from src.Dev import Dev
from pathlib import Path
from decimal import Decimal
from src.Discord import Discord
from src.TERMGUI.Run import Run
from src.TERMGUI.Log import Log
from src.Settings import Settings
from src.TERMGUI.Dialog import Dialog

class Update:
    def run():
        if Dev.get("DO_NOT_UPDATE"):
            Run.prg("pip", "freeze > requirements.txt")
            return True

        Update.pull_updates_from_git()
        return Update.run_migrations()

    def pull_updates_from_git():
        Run.prg("git", "pull --rebase")

    def install_pip_packages():
        Run.prg("pip", "install -r requirements.txt")
        if Dev.isDev():
            Run.prg("pip", "freeze > requirements.txt")

    def run_migrations():
        migrations      = glob("migrations/*")
        migrations.sort()
        migrations      = [ Path(x) for x in migrations ]
        current_version = Settings.get_version()
        result          = True

        for migration in migrations:
            migration_version = Decimal(migration.stem.replace("_","."))

            if migration_version > current_version:
                Update.install_pip_packages()

                ans = Run.prg("python", migration.absolute(), useSubprocess=True)

                if ans == 0:
                    args = { "type": "log", "content": Log.dump() }
                    Discord.notify(args)

                    Log(f'There was a problem loading this migration file!\n "{migration.absolute()}"',"warning")
                    Log.press_enter()
                    # If there was an issue upgrading the migration, we don't want to set the new version
                    return False
                elif ans != 1:
                    Log("You must restart the program to finish the update!","notice")
                    Log.press_enter()
                    result = False

                Settings.set_version(migration_version)

                # Push a notification to Discord
                content = f"{Settings.get_username(capitalize=True)} has upgraded to V{migration_version}!"
                args = { "type": "message", "content": content }
                Discord.notify(args)

        return result
