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
        return f'"{name.replace("_"," ")}"'.capitalize()

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

        # Attempt to send notification 5x
        i = 0
        while i < 5:
            try:
                requests.post(
                    self._get_endpoint_key(endpoint),
                    data    = json.dumps(data),
                    headers = Slack.headers,
                )

                i = 10
            except:
                i += 1
                Log(f'Slack notification refused to send! Try: {i}', "warning")

        if i != 10:
            # Slack notification failed 5x, skipping slack notification
            Log(f'Slack notification refused to send! Skipping notification..', "warning")

        if not quiet and i == 10:
            Log(f'Slack ({endpoint}): "{text}"')
            Log("Slack Notification Sent!")

    def _get_endpoint_key(self, endpoint):
        if endpoint == "dev":
            return Settings.get_key(Settings.slack_dev_key)
        elif endpoint == "prod":
            return Settings.get_key(Settings.slack_prod_key)

    def reset_slack_endpoints():
        Settings.set_key(Settings.slack_prod_key, "")
        Settings.set_key(Settings.slack_dev_key, "")
        Settings.set_slack_endpoints()

    def check_slack_endpoints():
        settings = Settings.get_all()

        if not Settings.slack_prod_key in settings or \
           not Settings.slack_dev_key in settings:
            return False

        if settings[Settings.slack_prod_key] == "" or \
           settings[Settings.slack_dev_key] == "":
            return False

        return True

    def set_slack_endpoints():
        if not Settings.check_slack_endpoints():
            drive = Drive()

            Settings.set_key(
                key  = Settings.slack_prod_key,
                data = drive.get_json_key(
                    remote_file    = f'{LOFSM_DIR_PATH}/db.json',
                    local_filepath = f'temp/db.json',
                    key            = Settings.slack_prod_key
                )
            )

            Settings.set_key(
                key  = Settings.slack_dev_key,
                data = drive.get_json_key(
                    remote_file    = f'{LOFSM_DIR_PATH}/db.json',
                    local_filepath = f'temp/db.json',
                    key            = Settings.slack_dev_key
                )
            )
