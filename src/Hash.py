import hashlib
from pathlib import Path
from src.Drive import Drive
from src.FileManagement.File import File
from src.env import LOFSM_DIR_PATH


class Hash:

    remote_db_fpath = f'{LOFSM_DIR_PATH}/db.json'
    temp_db_fpath   = f'temp/db.json'

    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.hash     = Hash.hash_file(filepath)
        self.drive    = Drive()

    def hash_file(filepath):
        filepath   = Path(filepath)
        BLOCK_SIZE = 1024*1024
        result     = hashlib.sha256()

        with open(filepath.absolute(), 'rb') as f:
            fb = f.read(BLOCK_SIZE)
            while len(fb) > 0:
                result.update(fb)
                fb = f.read(BLOCK_SIZE)

        return result.hexdigest()

    def push(self):
        if not self.drive.get_info(self.remote_db_fpath):
            File.set_json(
                filepath = self.temp_db_fpath,
                data     = {}
            )

            self.drive.set_json(
                remote_file    = self.remote_db_fpath,
                local_filepath = self.temp_db_fpath
            )

        self.drive.set_json_key(
            remote_file    = self.remote_db_fpath,
            local_filepath = self.temp_db_fpath,
            key            = self.filepath.name,
            data           = self.hash
        )

    def compare(self):
        remote_hash = self.drive.get_json_key(
            remote_file = self.remote_db_fpath,
            local_filepath = self.temp_db_fpath,
            key = self.filepath.name
        )

        if self.hash != remote_hash:
            return False

        return True
