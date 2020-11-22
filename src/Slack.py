import requests, json
from src.Dev import Dev
from src.Settings import Settings
from src.TERMGUI.Log import Log


class Slack:

    headers = {
        "Content-Type": "application/json"
    }

    endpoints = {
        "dev":  "slack_endpoint_dev",
        "prod": "slack_endpoint_prod",
    }

    def __init__(self, text, endpoint="prod"):
        endpoint = "dev" if Dev.isDev() else endpoint
        self._send_notification(text, endpoint)

    def get_nice_username():
        return Settings.get_username(capitalize=True)

    def make_nice_project_name(name):
        return f'"{name.replace("_"," ")}"'

    # PRIVATE

    def _send_notification(self, text, endpoint="prod"):
        data = { "text": text }

        Log("Sending Slack Notification..")

        requests.post(
            self._get_endpoint_key(endpoint),
            data    = json.dumps(data),
            headers = Slack.headers,
        )

        Log(f'Slack ({endpoint}): "{text}"')
        Log("Slack Notification Sent!")

    def _get_endpoint_key(self, endpoint):
        return Settings.get_key(Slack.endpoints[endpoint])
