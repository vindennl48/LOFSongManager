import filecmp
from pathlib import Path
from src.dev import Dev


# Definitions
EXTRACTED = Path("extracted_songs")
CACHED    = Path("compressed_songs")
TEMP      = Path("temp")


class Project:

    def __init__(self, entry):
        # entry argument is Database Entry Class
        self.entry = entry

    ## TESTS ##
    def is_dirty(self):
        if Dev.get("ALL_IS_DIRTY"):
            return True

        if self.get_song_file().exists() and self.get_song_file(version="original").exists():
            return not filecmp.cmp(
                self.get_song_file(),
                self.get_song_file(version="original"),
                shallow=False
            )

    def is_conflict(self):
        return self.get_song_file(version="yourversion").exists()

    def is_local(self):
        return self.get_root_dir().exists()

    def is_cached(self):
        return self.get_cache_file().exists()
    ## END TESTS ##

    ## FILEPATHS ##
    def get_root_dir(self):
        return EXTRACTED/self.entry.name

    def get_temp_dir(self):
        return TEMP/self.entry.name

    def get_cache_file(self):
        return CACHED/f'{self.entry.name}.lof'

    def get_song_file(self, version=None, temp=False):
        if not version:
            if temp:
                return self.get_temp_dir()/f'{self.entry.name}.song'
            return self.get_root_dir()/f'{self.entry.name}.song'

        if temp:
            return self.get_temp_dir()/f'{self.entry.name}_{version}.song'
        return self.get_root_dir()/f'{self.entry.name}_{version}.song'
    ## END FILEPATHS ##

