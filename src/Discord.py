import requests, json
from src.Dev import Dev
from src.Settings import Settings
from src.TERMGUI.Log import Log
from src.FileManagement.File import File

from discord_webhook import DiscordWebhook


class Discord:

    def __init__(self, content = "", quiet = False):
        self.content = content
        self.quiet = quiet
        self.dev = True if Dev.isDev() else False
        self.username = Settings.get_username(capitalize = True)

        self._set_endpoint()
        print(self.endpoint)

    def _set_endpoint(self):
        if self.dev:
            endpoint = self._dev_endpoint()
        else:
            endpoint = self._prod_endpoint()

        self.endpoint = endpoint

    def _dev_endpoint(self):
        return Settings.get_key(Settings.discord_dev_key)

    def _prod_endpoint(self):
        return Settings.get_key(Settings.discord_prod_key)

    def post(self):
        webhook = self._build_webhook()

        if not self.quiet:
            Log("Sending Discord notification...")
            Log(f'{webhook}')

        response = webhook.execute()

        if not self.quiet:
            if response.ok:
                Log("Notification webhook succeeded")
            else:
                Log('Notification webhook failed: {response}')

    def _build_webhook(self):
        url = self.endpoint
        content = self.content

        return DiscordWebhook(url = url, rate_limit_retry = True, content = content)


    def post_link(self, url, ID):
        name = self.username
        text = f'{name} uploaded {url}: https://drive.google.com/file/d/{ID}'

        self.content = text

        self.post()

    def reset_discord_endpoints():
        Settings.set_key(Settings.discord_prod_key, "")
        Settings.set_key(Settings.discord_dev_key, "")
        Settings.set_discord_endpoints()

    def check_discord_endpoints():
        settings = Settings.get_all()

        if not Settings.discord_prod_key in settings or \
           not Settings.discord_dev_key in settings:
            return False

        if settings[Settings.discord_prod_key] == "" or \
           settings[Settings.discord_dev_key] == "":
            return False

        return True

    def set_discord_endpoints():
        if not Settings.check_discord_endpoints():
            drive = Drive()

            Settings.set_key(
                key  = Settings.discord_prod_key,
                data = drive.get_json_key(
                    remote_file    = f'{LOFSM_DIR_PATH}/db.json',
                    local_filepath = f'temp/db.json',
                    key            = Settings.discord_prod_key
                )
            )

            Settings.set_key(
                key  = Settings.discord_dev_key,
                data = drive.get_json_key(
                    remote_file    = f'{LOFSM_DIR_PATH}/db.json',
                    local_filepath = f'temp/db.json',
                    key            = Settings.discord_dev_key
                )
            )
