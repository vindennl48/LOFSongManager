import requests
import json
from src.dev import dev
from src.settings.Settings import Settings
from src.helpers import log


class Notify:

    headers = { "Content-Type": "application/json" }

    def __init__(self, text):
        data = { "text": text }

        log("Sending Slack Notification..")

        requests.post(
            self.endpoint(),
            data = json.dumps(data),
            headers = self.headers,
        )

        log(f'Notify ({self.get_endpoint_key()}): "{text}"')
        log("Slack Notification Sent!")

    def get_endpoint_key(self):
        if dev("DEVELOPMENT"):
            return 'slack_endpoint_dev'
        else:
            return 'slack_endpoint_prod'

    def endpoint(self):
        return Settings.get()[self.get_endpoint_key()]

    def get_nice_username():
        return Settings.get_user(capitalize=True)

    def make_nice_project_name(name):
        return f'"{name.replace("_"," ")}"'
