import json
from glob import glob
from decimal import Decimal
from pathlib import Path
from src.helpers import pause
from src.Dev import Dev
from src.run.Run import Run
from src.settings.Settings import Settings
from src.env import VERSION
from src.slack.notify import Notify as Slack

class Update:
    def run():
        Update.pull_updates_from_git()
        result = Update.run_migrations()

        if Decimal(VERSION) != Settings.get_version():
            print("\n\n 'src.env.VERSION' does not match the current version!")
            print(" Please notify your administrator! \n\n")
            pause()

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
                Slack(f'{Settings.get_user(capitalize=True)} has upgraded to V{migration_version}!')

        return result
