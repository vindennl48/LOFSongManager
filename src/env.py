from src.dev import *

LOFSM_DIR_PATH         = "Audio/LOFSongManager"
LOFSM_DIR_HASH         = "1DEMYiL1aiRJYjf_B3QyKkUbow4xqNaJQ"
VERSION                = "1.0"
SLACK_WEBHOOK_BASE     = "https://hooks.slack.com/services/T0BQR9YTC/B01DNKG3FFB"
SLACK_WEBHOOK_ENDPOINT = "3gd2RRCXXzdJu0w7SIM8baeY"

if dev("DEVELOPMENT"):

    SLACK_WEBHOOK_ENDPOINT = "rckKja2hBgMdnMdVDdROdwOD"

    if dev("ALT_LOCATION"):
        LOFSM_DIR_PATH = "Audio/LOFSongManagerDev"
        LOFSM_DIR_HASH = "1CsUyd9rRiAxe_T8C1EwONWqrUgJS1blo"
