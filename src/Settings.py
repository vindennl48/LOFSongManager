from decimal import Decimal
from pathlib import Path
from src.Drive import Drive
from src.env import LOFSM_DIR_PATH
from src.FileManagement.File import File
from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog

class Settings:

    filepath       = Path(".settings")
    slack_prod_key = "slack_endpoint_prod"
    slack_dev_key  = "slack_endpoint_dev"

    def create():
        if not Settings.filepath.exists():
            File.set_json(Settings.filepath, {})
            Settings.set_username()
            Settings.set_version("0.0")
            Settings.set_slack_endpoints()

    def set_key(key, data):
        Settings.create()
        File.set_json_key(Settings.filepath.absolute(), key, data)

    def get_key(key):
        Settings.create()
        return File.get_json_key(Settings.filepath.absolute(), key)

    def get_all():
        Settings.create()
        return File.get_json(Settings.filepath.absolute())

    def set_version(version):
        Settings.set_key("version", str(version))

    def get_version():
        version = Settings.get_key("version")

        if not version:
            version = "0.0"
            Settings.set_key("version", version)

        return Decimal(version)

    def set_username():
        dialog = Dialog(
            title = "Welcome!",
            body = [
                f'Since this is your first time using this software, we',
                f'need to know your name to get things working smoothly!',
                f'\n',
                f'\n',
                f'What is your first name?',
            ]
        )

        Settings.set_key(
            "username",
            dialog.get_result("Name").lower()
        )

    def get_username(capitalize=False):
        username = Settings.get_key("username")

        if capitalize:
            username = username.capitalize()

        return username

    def reset_slack_endpoints():
        Settings.set_key(Settings.slack_prod_key, "")
        Settings.set_key(Settings.slack_dev_key, "")
        Settings.set_slack_endpoints()

    def check_slack_endpoints():
        settings = Settings.get_all()

        if not Settings.slack_prod_key in settings or \
           not Settings.slack_dev_key in settings:
            return False

        if settings[Settings.slack_prod_key] == "" or \
           settings[Settings.slack_dev_key] == "":
            return False

        return True

    def set_slack_endpoints():
        if not Settings.check_slack_endpoints():
            drive = Drive()

            Settings.set_key(
                key  = Settings.slack_prod_key,
                data = drive.get_json_key(
                    remote_file    = f'{LOFSM_DIR_PATH}/db.json',
                    local_filepath = f'temp/db.json',
                    key            = Settings.slack_prod_key
                )
            )

            Settings.set_key(
                key  = Settings.slack_dev_key,
                data = drive.get_json_key(
                    remote_file    = f'{LOFSM_DIR_PATH}/db.json',
                    local_filepath = f'temp/db.json',
                    key            = Settings.slack_dev_key
                )
            )
