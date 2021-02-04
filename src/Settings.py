from decimal import Decimal
from pathlib import Path
from src.FileManagement.File import File
from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog

class Settings:

    filepath       = Path(".settings")
    slack_prod_key = "slack_endpoint_prod"
    slack_dev_key  = "slack_endpoint_dev"

    def create():
        if not Settings.filepath.exists():
            File.set_json(Settings.filepath.absolute(), {})
            Settings.set_username()
            Settings.set_version("0.0")
            Settings.set_slack_endpoints()

    def set_key(key, data):
        Settings.create()
        File.set_json_key(Settings.filepath.absolute(), key, data)

    def get_key(key):
        Settings.create()
        return File.get_json_key(Settings.filepath.absolute(), key)

    def delete_key(key):
        settings = Settings.get_all()
        settings.pop(key, None)
        Settings.set_all(settings)

    def get_all():
        Settings.create()
        return File.get_json(Settings.filepath.absolute())

    def set_all(data):
        Settings.create()
        return File.set_json(Settings.filepath.absolute(), data)

    def set_version(version):
        Settings.set_key("version", str(version))

    def get_version():
        version = Settings.get_key("version")

        if not version:
            version = "0.0"
            Settings.set_version(version)

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
