from glob import glob
from pathlib import Path
from src.TERMGUI.Log import Log
from src.FileManagement.File import File


class DummyFiles:
    def __init__(self, filepath):
        self.filepath  = Path(filepath)
        self.json_path = Path(self.filepath / "dummy.json")

    def exists(self):
        if json_file.exists():
            return True
        return False

    def is_in_max(self, file_stem):
        if file_stem in self.get_max():
            return True
        return False

    def get_list(self):
        return self.get_dummy_data()["dummy"]

    def get_max(self):
        return self.get_dummy_data()["max"]

    def get_dummy_data(self):
        json_file = File.get_json(self.json_path)

        if not json_file:
            json_file = {"max": {},"dummy": []}

        return json_file

    def set_dummy_data(self, json_file):
        File.set_json(self.json_path, json_file)

    def get_wav_files(self):
        wavs = glob(f"{self.filepath.absolute()}/*.wav")
        return [ Path(x).name for x in wavs ]

    def create(self):
        # Just make sure theres no dummy files first
        self.remove()

        wavs      = self.get_wav_files()
        json_file = self.get_dummy_data()

        for wav in wavs:
            file_stem, num, ext = File.split_name(wav)

            if not file_stem in json_file['max']:
                json_file['max'][file_stem] = num
            else:
                if num > json_file['max'][file_stem]:
                    json_file['max'][file_stem] = num

        for file_stem in json_file['max']:
            num = json_file['max'][file_stem]

            for i in range(num):
                if i == 0:
                    path = Path(f"{self.filepath}/{file_stem}.{ext}")
                else:
                    path = Path(f"{self.filepath}/{file_stem}({i}).{ext}")

                if not path.exists():
                    path.touch()
                    json_file['dummy'].append(path.name)

        self.set_dummy_data(json_file)

        return self

    def remove(self):
        json_file = self.get_dummy_data()

        for file in json_file['dummy']:
            file = Path(f"{self.filepath}/{file}")
            if file.stat().st_size == 0:
                file.unlink()

        json_file['dummy'] = []
        self.set_dummy_data(json_file)
