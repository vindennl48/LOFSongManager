import hashlib
from pathlib import Path
from src.Drive import Drive
from src.TERMGUI.Log import Log
from src.FileManagement.File import File
from src.env import LOFSM_DIR_PATH


class Hash:

    remote_db_fpath = f'{LOFSM_DIR_PATH}/db.json'
    temp_db_fpath   = f'temp/db.json'

    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.hash     = Hash.hash_file(filepath)
        self.drive    = Drive()

    def remove(self):
        self.drive.remove_json_key(
            remote_file    = Hash.remote_db_fpath,
            local_filepath = Hash.temp_db_fpath,
            key            = self.filepath.name
        )

    def push(self):
        # Make sure hash is up-to-date
        self._re_hash()

        # You must check this function during use!
        if not self.hash:
            Log(f'Can not push hash for "{self.filepath.name}"!', "warning")
            Log(f'Local compressed project doesn\'t exist!', "warning")
            return False

        # Create remote db.json if it doesn't exist
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

        return True

    def compare(self):
        if not self.hash:
            return False

        remote_hash = self.drive.get_json_key(
            remote_file    = self.remote_db_fpath,
            local_filepath = self.temp_db_fpath,
            key            = self.filepath.name
        )

        if self.hash != remote_hash:
            return False

        return True

    # Static
    def hash_file(filepath):
        filepath   = Path(filepath)
        BLOCK_SIZE = 1024*1024
        result     = hashlib.sha256()

        if not filepath.exists():
            return None

        with open(filepath.absolute(), 'rb') as f:
            fb = f.read(BLOCK_SIZE)
            while len(fb) > 0:
                result.update(fb)
                fb = f.read(BLOCK_SIZE)

        return result.hexdigest()

    # Private
    def _re_hash(self):
        self.hash = Hash.hash_file(self.filepath)

