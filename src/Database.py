import json
from pathlib import Path
from src.Drive import Drive
from src.Settings import Settings
from src.FileManagement.File import File


# Definitions
DATABASE_FILENAME     = "db.json"
KEY_CLOUD_DATABASE_ID = "cloud_database_id"
FILEPATH_LOCAL        = f'temp/{DATABASE_FILENAME}'

DEFAULT_DATABASE = {
    "projects": {},
    "data":     {}
}


class Entry:
    # This class exists as a database entry.
    # When getting a search result from the Database class below,
    #  it will return one of these classes.  This allows the user
    #  to save directly to this class, and it will update the
    #  database for you.
    #
    # Trying to make this like a postgres rails setup

    def __init__(self, model, name, data):
        self.model = model
        self.name  = name
        self.data  = data

    def update(self):
        Database.set_entry(self.model, self.name, self.data)

    def refresh(self):
        self.data = Database.get_entry(self.model, self.name)


class Database:
    cloud_id = None   # Remote cloud id

    def initialize():
        Database.cloud_id = Database.get_cloud_id()

        # Download a fresh version of the database
        Database.refresh()

    def get_entry(model, name):
        db = File.get_json(FILEPATH_LOCAL)

        if model in db:
            if name in db[model]:
                return Entry(model, name, db[model][name])

        return None

    def get_all(model):
        db = File.get_json(FILEPATH_LOCAL)
        entries = None

        if model in db:
            entries = [ Entry(model, name, db[model][name]) for name in db[model] ]

        return entries

    def set_entry(model, name, data):
        # Before updating the database, make sure we are up-to-date
        Database.refresh()

        db = File.get_json(FILEPATH_LOCAL)

        if model in db:
            db[model][name] = data
            File.set_json(FILEPATH_LOCAL, db)
            return Drive.upload(FILEPATH_LOCAL, Drive.mimeType["json"])

        raise Exception(f'Model "{model}" doesn\'t exist in Database!')

    def refresh():
        File.delete(FILEPATH_LOCAL)
        Drive.download(Database.cloud_id, FILEPATH_LOCAL)

    def get_cloud_id():
        # Check if 'cloud_database_id' exists in .settings
        result = Settings.get_key(KEY_CLOUD_DATABASE_ID)

        # If no id is found, lets find it
        if not result:
            result = Drive.get_id(DATABASE_FILENAME)

        # if still no id is found, create new db.json file
        if not result:
            result = Database.create_database()

        # Something is wrong, can not get id of database nor create
        #  a new database on the cloud..
        if not result:
            raise Exception("Database.cloud_id can not be found!")

        # Save id to settings
        Settings.set_key(KEY_CLOUD_DATABASE_ID, result)

        return result

    def create_database():
        with open(FILEPATH_LOCAL, "w") as f:
            json.dump(DEFAULT_DATABASE, f, indent=4)

        return Drive.upload(FILEPATH_LOCAL, Drive.mimeType["json"])

Database.initialize()
