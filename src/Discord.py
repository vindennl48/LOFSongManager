import requests, json
from src.Dev import Dev
from src.Settings import Settings
from src.TERMGUI.Log import Log

from discord_webhook import DiscordWebhook


class Discord:

    dev_endpoint = Settings.get_key(Settings.discord_dev_key)
    prod_endpoint = Settings.get_key(Settings.discord_prod_key)

    def __init__(self, quiet = False):
        self.content = content
        self.quiet = quiet

        self.dev = True if Dev.isDev() else False
        self.username = Settings.get_username(capitalize = True)

        self.set_endpoint()

    def set_endpoint(self):
        if self.dev:
            endpoint = self.dev_endpoint
        else:
            endpoint = self.prod_endpoint

        self.endpoint = endpoint

    def post(self):
        self.webhook = self.build_webhook()
        self.response = self.webhook.execute()

        self.log_request_response()

    def build_webhook(self):
        return DiscordWebhook(
                url = self.endpoint,
                rate_limit_retry = True,
                content = self.content)

    def log_request_response(self):
        if self.quiet:
            return None

        if not self.response:
            Log("Notification webhook did not complete:")
            Log(f"  Webhook: {inspect.getmembers(self.webhook)}")

        if not self.response.ok:
            Log("Notification webhook failed:")
            Log(f"  Webhook: {inspect.getmembers(self.webhook)}")
            Log(f"  Response: {inspect.getmembers(self.response)}")
        else:
            Log("Notification webhook succeeded:")
            Log(f"  Webhook: {inspect.getmembers(self.webhook)}")
            Log(f"  Response: {inspect.getmembers(self.response)}")

    def post_link(self, link_title, url):
        description = f"{self.username} uploaded {link_title}"

        self.content = f"{description}: {url}"

        self.post()

    def post_message(self, content):
        self.content = content

        self.post()

    def post_log(self, content, quiet = True):
        log = f"{self.username} – Log: {content}"

        self.content = log
        self.quiet = quiet
        self.dev = True

        self.post()
