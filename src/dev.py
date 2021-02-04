from src.TERMGUI.Log import Log
from src.FileManagement.File import File

class Dev:

    filepath = ".dev"

    def isDev():
        return Dev.get("DEVELOPMENT")

    def get(key):
        data = Dev._get_data()

        if key in data:
            if data[key]:
                Log(f'Development Mode: {key}',"warning")
                Log.press_enter()
            return data[key]
        else:
            data[key] = False
            File.set_json(Dev.filepath, data)
            return False

    # PRIVATE

    def _get_data():
        json_file = File.get_json(Dev.filepath)

        if not json_file:
            json_file = { "DEVELOPMENT": False, }

            File.set_json(
                filepath = Dev.filepath,
                data     = json_file
            )

        return json_file
