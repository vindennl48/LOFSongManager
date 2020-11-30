import requests, json
from src.dev import Dev
from src.Settings import Settings
from src.TERMGUI.Log import Log
from src.FileManagement.File import File


class Slack:

    headers = {
        "Content-Type": "application/json"
    }

    def __init__(self, text, endpoint="prod", quiet=False):
        endpoint = "dev" if Dev.isDev() else endpoint
        self._send_notification(text, endpoint, quiet)

    def get_nice_username():
        return Settings.get_username(capitalize=True)

    def make_nice_project_name(name):
        return f'"{name.replace("_"," ")}"'

    def upload_log():
        log = File.get(Log.filepath)
        Slack(
            text     = f'{Settings.get_username(capitalize=True)} Log',
            endpoint = "dev",
            quiet    = True
        )
        Slack(
            text     = log,
            endpoint = "dev",
            quiet    = True
        )

    def send_link(link_name, ID):
        username = Slack.get_nice_username()
        link     = f'{username} uploaded {link_name}: https://drive.google.com/file/d/{ID}'
        Slack(link)

    # PRIVATE

    def _send_notification(self, text, endpoint="prod", quiet=False):
        data = { "text": text }

        if not quiet:
            Log("Sending Slack Notification..")

        requests.post(
            self._get_endpoint_key(endpoint),
            data    = json.dumps(data),
            headers = Slack.headers,
        )

        if not quiet:
            Log(f'Slack ({endpoint}): "{text}"')
            Log("Slack Notification Sent!")

    def _get_endpoint_key(self, endpoint):
        if endpoint == "dev":
            return Settings.get_key(Settings.slack_dev_key)
        elif endpoint == "prod":
            return Settings.get_key(Settings.slack_prod_key)
