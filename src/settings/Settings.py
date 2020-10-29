import json
from decimal import Decimal
from src.helpers import clear_screen
from pathlib import Path

class Settings:

    file = Path(".settings")

    def create():
        if not Settings.file.exists():
            # Create the actual .settings file
            settings = {}
            with open(Settings.file.absolute(), 'w') as f:
                json.dump(settings, f)

            # Add necessary values to .settings
            Settings.set_user()
            Settings.set_version("0.0")
            Settings.set_slack_endpoints()

    def get():
        Settings.create()

        with open(Settings.file.absolute()) as f:
            result = json.load(f)

        return result

    def set(settings):
        Settings.create()

        with open(Settings.file.absolute(), 'w') as f:
            json.dump(settings, f)

    def set_version(version):
        settings = Settings.get()
        settings["version"] = str(version)
        Settings.set(settings)

    def get_version():
        settings = Settings.get()

        if not "version" in settings:
            Settings.set_version("0.0")

        return Decimal(Settings.get()["version"])

    def set_user():
        settings = Settings.get()

        output = [
            f'',
            f'',
            f'  :: Welcome!',
            f'',
            f'     Since this is your first time using this software, we ',
            f'     need to know your name to get things working smoothly!',
            f'',
            f'     What is your first name?',
            f'',
        ]
        print( "\n".join(output) )

        user = input("Name: ").lower()

        print('\n   Thanks!!\n')

        settings['user'] = user

        Settings.set(settings)

    def get_user(capitalize=False):
        user = Settings.get()["user"]

        if capitalize:
            return user.capitalize()

        return user

    def set_slack_endpoints():
        settings = Settings.get()

        output = [
            f'',
            f'',
            f'  :: Slack integration setup',
            f'',
            f'     Enter the production and development webhook URLs to finish',
            f'     setting up the Slack integration. The URLs are listed on the',
            f'     Drive here:',
            f'',
            f'       ---> https://drive.google.com/file/d/1xfqoWJN_bLi8E0f7n5eRbWxf1uDALKB7/view?usp=sharing',
            f'',
            f'',
        ]

        print( "\n".join(output) )

        settings["slack_endpoint_prod"] = input('Production endpoint URL: ').lower()
        settings["slack_endpoint_dev"]  = input('Development endpoint URL: ').lower()

        Settings.set(settings)
