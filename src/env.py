from src.Dev import Dev

LOFSM_DIR_PATH = "Audio/LOFSongManager"
LOFSM_DIR_HASH = "1DEMYiL1aiRJYjf_B3QyKkUbow4xqNaJQ"
VERSION        = "1.2"

if Dev.isDev():
    if Dev.get("ALT_LOCATION"):
        LOFSM_DIR_PATH = "Audio/LOFSongManagerDev"
        LOFSM_DIR_HASH = "1CsUyd9rRiAxe_T8C1EwONWqrUgJS1blo"
