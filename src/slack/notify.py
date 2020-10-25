import requests
import json


class Notify:

    endpoint = "https://hooks.slack.com/services/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"
    headers = { "Content-Type": "application/json" }

    def __init__(self, text):
        data = { "text": text }

        requests.post(
            self.endpoint,
            data = json.dumps(data),
            headers = self.headers,
        )
