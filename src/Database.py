import json
from pathlib import Path
from src.Drive import Drive
from src.TERMGUI.Log import Log
from src.Settings import Settings
from src.FileManagement.File import File


# Definitions
DATABASE_FILENAME = "db.json"
FILEPATH_LOCAL    = Path(f'temp/{DATABASE_FILENAME}')

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

    # Save changes from self.data to cloud database
    def update(self):
        return Database.set_entry(self.model, self.name, self.data)

    # Check to see if project exists in database, if it does, update entry
    def sync(self):
        result = Database.get_entry(self.model, self.name)
        if result:
            self.data = result.data
        return True

    # Pull down any updates from the cloud database
    def refresh(self):
        Database.refresh()
        return self.sync()

    def destroy(self):
        return Database.destroy_entry(self.model, self.name)


class Database:
    cloud_id = None   # Remote cloud id

    def initialize():
        Database.cloud_id = Database.get_cloud_id()

        # Download a fresh version of the database
        Database.refresh()

    # Just in case the database was erased
    def local_check():
        if not FILEPATH_LOCAL.exists():
            Database.refresh()

    def get_entry(model, name):
        Database.local_check()

        db = File.get_json(FILEPATH_LOCAL)

        if model in db:
            if name in db[model]:
                return Entry(model, name, db[model][name])

        return None

    def get_all(model):
        Database.local_check()

        db = File.get_json(FILEPATH_LOCAL)
        entries = None

        if model in db:
            entries = [ Entry(model, name, db[model][name]) for name in db[model] ]

        return entries

    def set_entry(model, name, data):
        # If there is no 'id' then user needs to upload the project first!
        if not data["id"]:
            return False

        # Before updating the database, make sure we are up-to-date
        Database.refresh()

        db = File.get_json(FILEPATH_LOCAL)

        if model in db:
            db[model][name] = data
            File.set_json(FILEPATH_LOCAL, db)
            return Database.push()

        raise Exception(f'Model "{model}" doesn\'t exist in Database!')

    def destroy_entry(model, name):
        Database.refresh()

        db = File.get_json(FILEPATH_LOCAL)

        if model in db:
            db[model].pop(name)
            File.set_json(FILEPATH_LOCAL, db)
            return Database.push()

        raise Exception(f'Model "{model}" doesn\'t exist in Database!')

    def refresh():
        File.delete(FILEPATH_LOCAL)
        Drive.download(Database.cloud_id, FILEPATH_LOCAL)

    def push():
        if FILEPATH_LOCAL.exists():
            return Drive.upload(FILEPATH_LOCAL, Drive.mimeType["json"])
        return False

    def get_cloud_id():
        result = Drive.get_id(DATABASE_FILENAME)

        if not result:
            result = Database.create_database()

        # Something is wrong, can not get id of database nor create
        #  a new database on the cloud..
        if not result:
            raise Exception("Database.cloud_id can not be found!")

        return result

    def create_database():
        with open(FILEPATH_LOCAL, "w") as f:
            json.dump(DEFAULT_DATABASE, f, indent=4)

        return Drive.upload(FILEPATH_LOCAL, Drive.mimeType["json"])

Database.initialize()
