from glob import glob
from decimal import Decimal
from pathlib import Path
from src.Dev import Dev
from src.TERMGUI.Run import Run
from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog
from src.Settings import Settings
from src.env import VERSION
# from src.slack.notify import Notify as Slack

class Update:
    def run():
        if Dev.get("DO_NOT_UPDATE"):
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
                    Slack.upload_log()
                    Log(f'There was a problem loading this migration file!\n "{migration.absolute()}"',"warning")
                    Log.press_enter()
                    # If there was an issue upgrading the migration, we don't want to set the new version
                    return False
                elif ans != 1:
                    Log("You must restart the program to finish the update!","notice")
                    Log.press_enter()
                    result = False

                Settings.set_version(migration_version)

                # Push a notification to Slack
                Slack(f'{Settings.get_user(capitalize=True)} has upgraded to V{migration_version}!')

        return result
