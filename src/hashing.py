import hashlib
import json
from pathlib import Path
from src.helpers import *
from src.Drive import Drive
from src.env import LOFSM_DIR_HASH
from src.env import LOFSM_DIR_PATH

def hash_file(file):
    file       = Path(file)
    BLOCK_SIZE = 1024*1024
    result     = hashlib.sha256()

    with open(file.absolute(), 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            result.update(fb)
            fb = f.read(BLOCK_SIZE)

    return result.hexdigest()

def get_local_db():
    db_path = Path(f"compressed_songs/db.json")
    db      = {}

    # if json file doesnst exist, create it
    if not db_path.exists():
        with open(db_path.absolute(), 'w') as f:
            json.dump(db, f)

    # open json file
    with open(db_path.absolute()) as f:
        db = json.load(f)

    return db

def set_local_db(key, value):
    db_path = Path(f"compressed_songs/db.json")
    db      = get_local_db()
    db[key] = value

    with open(db_path.absolute(), 'w') as f:
        json.dump(db, f)

def rm_local_db(key):
    db_path = Path(f"compressed_songs/db.json")
    db      = get_local_db()
    db.pop(key, None)

    with open(db_path.absolute(), 'w') as f:
        json.dump(db, f)

def check_local_db(key):
    db_path = Path(f"compressed_songs/db.json")
    db      = get_local_db()
    if key in db:
        return True
    return False

def get_remote_db_raw(drive):
    return drive.get_info(search=f'{LOFSM_DIR_PATH}/db.json')

def get_remote_db(drive):
    temp_db      = {}
    temp_db_path = Path('temp/db.json')

    try:
        remote_db = drive.get_info(search=f"{LOFSM_DIR_PATH}/db.json")
        if not remote_db:
            raise Exception('No File Exists! "db.json"')
    except Exception as e:
        print(f"Error: {e}")
        raise Exception("\n\n## An error has occurred while downloading db.json.. ##\n")

    # download and open db.json
    drive.download(remote_db['id'], temp_db_path.absolute())
    with open(temp_db_path.absolute()) as f:
        temp_db = json.load(f)

    return temp_db

def set_remote_db(drive, key, value):
    temp_db_path = Path('temp/db.json')
    temp_db      = get_remote_db(drive)
    temp_db[key] = value

    with open(temp_db_path.absolute(), 'w') as f:
        json.dump(temp_db, f)

    drive.update(temp_db_path.absolute(), Drive.mimeType['json'], get_remote_db_raw(drive)['id'])

def rm_remote_db(drive, key):
    temp_db_path = Path('temp/db.json')
    temp_db      = get_remote_db(drive)
    temp_db.pop(key, None)

    with open(temp_db_path.absolute(), 'w') as f:
        json.dump(temp_db, f)

    drive.update(temp_db_path.absolute(), Drive.mimeType['json'], get_remote_db_raw(drive)['id'])

def check_remote_db(drive, key):
    temp_db_path = Path('temp/db.json')
    temp_db      = get_remote_db(drive)
    if key in temp_db:
        return True
    return False

def compare_hash(drive, name):
    db        = get_local_db()
    remote_db = get_remote_db(drive)

    if name in db and name in remote_db:
        if db[name] == remote_db[name]:
            log("Hashes match!")
            return True

    if not name in remote_db:
        raise Exception("\n\n## There is no hash for this project on remote db.json! ##\n## Alert your administrator! ##")

    log("Hashes do not match!")
    return False

def set_local_hash_from_file(name, path):
    log("Setting local hash from file")
    path = Path(path)
    hf   = hash_file(path.absolute())
    set_local_db(name, hf)
    log("Finished setting hash!")

def set_local_hash_from_remote(drive, name):
    log("Setting local hash from remote")
    remote_db = get_remote_db(drive)
    set_local_db(name, remote_db[name])
    log("Finished setting local hash!")

def set_remote_hash_from_local(drive, name):
    log("Setting remote hash from local")
    db = get_local_db()
    if name in db:
        set_remote_db(drive, name, db[name])
    else:
        raise Exception(f"Key 'name' is not in local db.json!")
    log("Finished setting remote hash!")
