import requests
import json
from src.dev import dev
from src.helpers import get_settings


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
        endpoint_key = ''
        settings = get_settings()

        if dev("DEVELOPMENT"):
            endpoint_key = 'slack_endpoint_dev'
        else:
            endpoint_key = 'slack_endpoint_prod'

        return settings[endpoint_key]
