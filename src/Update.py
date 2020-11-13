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
        result = Update.run_migrations()

        if Decimal(VERSION) != Settings.get_version():
            Dialog(
                title = "Version Mismatch!",
                body  = [
                    f'src.env.VERSION does not match the current version!',
                    f'The version number was not updated properly.',
                    f'\n',
                    f'\n',
                    f'Please notify your administrator!',
                    f'\n',
                    f'\n',
                ],
                clear = False
            )
            Log.press_enter()

        return result

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
                    raise Exception(f'There was a problem loading this migration file!\n "{migration.absolute()}"')
                elif ans != 1:
                    result = False

                Settings.set_version(migration_version)

                # Push a notification to Slack
                # Slack(f'{Settings.get_user(capitalize=True)} has upgraded to V{migration_version}!')

        return result
