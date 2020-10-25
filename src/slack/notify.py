import requests
import json
from src.env import *


class Notify:

    headers = { "Content-Type": "application/json" }

    def __init__(self, text):
        data = { "text": text }

        requests.post(
            self.endpoint(),
            data = json.dumps(data),
            headers = self.headers,
        )

    def endpoint(self):
        return f'{SLACK_WEBHOOK_BASE}/{SLACK_WEBHOOK_ENDPOINT}'
