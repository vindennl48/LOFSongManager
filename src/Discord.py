import requests, json, pprint
from src.Dev import Dev
from src.Settings import Settings
from src.TERMGUI.Log import Log
from src.FileManagement.File import File
from discord_webhook import DiscordWebhook as Webhook


class Discord:

    def __init__(self, text, endpoint="prod", quiet=False):
        endpoint = "dev" if Dev.isDev() else endpoint
        self._send_notification(text, endpoint, quiet)

    def get_nice_username():
        return Settings.get_username(capitalize=True)

    def make_nice_project_name(name):
        return f'"{name.replace("_"," ")}"'.capitalize()

    def upload_log():
        log = File.get(Log.filepath)
        Discord(
            text     = f'{Settings.get_username(capitalize=True)} Log',
            endpoint = "dev",
            quiet    = True
        )
        Discord(
            text     = log,
            endpoint = "dev",
            quiet    = True
        )

    def send_link(link_name, ID):
        username = Discord.get_nice_username()
        link     = f'{username} uploaded {link_name}: https://drive.google.com/file/d/{ID}'
        Discord(link)

    # PRIVATE

    def _send_notification(self, text, endpoint="prod", quiet=False):
        if not quiet:
            Log("Sending Discord Notification..")

        endpoint = self._get_endpoint_key(endpoint)
        request = self._build_webhook(endpoint, text)

        response = request.execute()

        if not quiet:
            formatted_request = self._format_log_line(request)

            if not response:
                Log("Notification webhook did not complete:", "warning")
                Log(f"Webhook:{formatted_request}", "sub")
            else:
                formatted_response = self._format_log_line(response)

                if not response.ok:
                    Log("Notification webhook failed:", "warning")
                    Log(f"Webhook:{formatted_request}", "sub")
                    Log(f"Response:{formatted_response}", "sub")
                else:
                    Log("Notification webhook succeeded:", "notice")

    def _get_endpoint_key(self, endpoint):
        if endpoint == "dev":
            return Settings.get_key(Settings.discord_dev_key)
        elif endpoint == "prod":
            return Settings.get_key(Settings.discord_prod_key)

    def _build_webhook(self, url, content):
        return Webhook(url = url, rate_limit_retry = True, content = content)

    def _format_log_line(self, text):
        return f"\n\n{pprint.pformat(vars(text))}\n\n"
