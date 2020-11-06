from src.File import File

class Dev:

    filepath = ".dev"

    def __init__(self, key):
        Dev.get(key)

    def isDev():
        return Dev.get("DEVELOPMENT")

    def get(key):
        data = Dev.get_data()

        if key in data:
            return data[key]
        else:
            data[key] = False
            File.set_json(Dev.filepath, data)
            return False

    def get_data():
        return File.get_json_or_create(
            Dev.filepath,
            {
                "DEVELOPMENT": False,
            }
        )
