import json
from pathlib import Path

class File:
    def append(filepath, text):
        filepath = Path(filepath)

        with open(filepath.absolute(), "a") as f:
            f.write(f'{text}\n')

    def delete(filepath):
        filepath = Path(filepath)

        if filepath.exists():
            filepath.unlink()

    def get_json(filepath):
        filepath = Path(filepath)
        result   = None

        if filepath.exists():
            with open(filepath.absolute()) as f:
                result = json.load(f)

        return result

    def set_json(filepath, data):
        filepath = Path(filepath)

        with open(filepath.absolute(), "w") as f:
            json.dump(data, f, indent=4)

    def set_json_key(filepath, key, data):
        json_file      = File.get_json(filepath)
        json_file[key] = data
        File.set_json(filepath, json_file)

    def get_json_key(filepath, key):
        json_file = File.get_json(filepath)
        if not key in json_file:
            return None
        return json_file[key]
