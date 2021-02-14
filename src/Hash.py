import hashlib, json
from pathlib import Path
from src.Drive import Drive
from src.TERMGUI.Log import Log
from src.FileManagement.File import File


# Definitions
DATABASE_FILENAME = "hash.json"
FILEPATH_LOCAL    = Path(f'compressed_songs/{DATABASE_FILENAME}')
DEFAULT_DATABASE  = {}

class Hash:
    # This class only deals with the local cache'd compressed songs
    #  To update the hash on the cloud/remote server, you must update
    #  through the project's 'entry' object.

    def initialize():
        if not FILEPATH_LOCAL.exists():
            Hash.create_database()

    def get_project_hash(project):
        db = File.get_json(FILEPATH_LOCAL)

        if not project.entry.name in db:
            Log(f'No local hashes exist for song "{project.entry.name}"!',"warning")
            # Log.press_enter()
            return False

        return db[project.entry.name]

    def set_project_hash(project, hash):
        if not hash:
            return False

        File.set_json_key(FILEPATH_LOCAL, project.entry.name, hash)

        return True

    def remove_project_hash(project):
        db = File.get_json(FILEPATH_LOCAL)
        if project.entry.name in db:
            db.pop(project.entry.name)
        File.set_json(FILEPATH_LOCAL, db)
        return True

    def create_database():
        # If database doesn't exist, make one
        if not FILEPATH_LOCAL.exists():
            with open(FILEPATH_LOCAL, "w") as f:
                json.dump(DEFAULT_DATABASE, f, indent=4)

    def create_hash_from_project(project):
        filepath   = project.get_cache_file()
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


Hash.initialize()
