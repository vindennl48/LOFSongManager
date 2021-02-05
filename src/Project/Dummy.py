from copy import deepcopy
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder

# Definitions
FOLDERS            = [ "Media", "Bounces" ]
DEFAULT_DUMMY_JSON = { "max": {} }

class Dummy:
    def set_dummy_files(self):
        # double check that the dummy.json files exist
        self.create_dummy_json()

        for folder in FOLDERS:
            folder     = self.get_root_dir()/folder
            dummy_json = folder/"dummy.json"
            data       = File.get_json(dummy_json)
            wavs       = Folder.ls_files(folder, "wav")

            # Lets find the max wav numbers
            for wav in wavs:
                file_stem, num, ext = File.split_name(wav)

                if not file_stem in data["max"]:
                    data["max"][file_stem] = num
                else:
                    if num > data["max"][file_stem]:
                        data["max"][file_stem] = num

            # Now lets create the dummy files if they don't already exist
            for file_stem in data["max"]:
                num = data["max"][file_stem]

                for i in range(num):
                    if i == 0:
                        path = folder/f'{file_stem}.wav'
                    else:
                        path = folder/f'{file_stem}({i}).wav'

                    path.touch()

            # Lets also get rid of the "dummy" key that is unused now
            if "dummy" in data:
                data.pop("dummy")

            # Lastly, lets update the dummy.json file
            File.set_json(dummy_json, data)

    def remove_dummy_files(self):
        # Remove any wav files that are 0 bytes in size
        for folder in FOLDERS:
            folder = self.get_root_dir()/folder
            wavs   = Folder.ls_files(folder, "wav")
            for wav in wavs:
                if wav.exists() and wav.stat().st_size == 0:
                    wav.unlink()

    def create_dummy_json(self):
        # Create all dummy.json files if they don't exist
        for folder in FOLDERS:
            folder     = self.get_root_dir()/folder
            dummy_json = folder/"dummy.json"
            if not dummy_json.exists():
                data = deepcopy(DEFAULT_DUMMY_JSON)
                File.set_json(dummy_json, data)

