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
        result   = {}

        if filepath.exists():
            with open(filepath.absolute()) as f:
                result = json.load(f)

        return result

    def set_json(filepath, data):
        filepath = Path(filepath)

        with open(filepath.absolute(), "w") as f:
            json.dump(data, f, indent=4)

    def get_json_or_create(filepath, data):
        filepath = Path(filepath)

        if filepath.exists():
            return File.get_json(filepath)
        else:
            File.set_json(filepath, data)
            return data
