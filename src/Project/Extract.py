from src.Tar import Tar
from src.TERMGUI.Log import Log
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder

class Extract:

    def extract_project(self):
        Log("Extracting project..")

        # Clean out temp project if it exists
        Log("Cleaning out temp folder")
        Folder.delete( self.get_temp_dir() )

        # Extract cache to 'temp' folder
        Log("Extracting project")
        Tar.extract( self.get_cache_file(), self.get_temp_dir() )

        # Create required folders in 'extracted_songs'
        self.create_required_folders()

        # Copy and convert from 'temp' to 'extracted_songs'
        if not self.move_temp_to_extracted_songs():
            # If function fails, remove broken extracted project
            # to prevent issues trying again.
            Folder.delete( self.get_root_dir() )
            Log("Could not move project from 'temp' to 'extracted_songs'..","warning")
            Log.press_enter()
            return False

        return True

    def create_required_folders(self, temp=False):
        # Need to make sure these folders exist
        Log("Creating necessary folders")
        for location in ["Media","Bounces","Mixdown"]:
            if temp:
                Folder.create( self.get_temp_dir()/location )
            Folder.create( self.get_root_dir()/location )

    def move_temp_to_extracted_songs(self):
        # Convert mp3's to wav's
        for location in ["Media", "Bounces"]:
            Log(f'Converting "{location}" mp3\'s to wav\'s')
            if not Audio.folder_to_wav( self.get_temp_dir()/location, self.get_root_dir()/location ):
                return False

            Log(f'Copying over "{location}" dummy.json')
            if self.get_dummy_db(location, temp=True).exists():
                File.recursive_overwrite(
                    self.get_dummy_db(location, temp=True),
                    self.get_dummy_db(location, temp=False),
                )

        # Copy over the previous mixdowns
        Log("Copying over 'Mixdown' mp3's")
        Folder.copy( self.get_temp_dir()/"Mixdown", self.get_root_dir()/"Mixdown" )

        # Copy over the song file
        Log("Copying over Studio One project file")
        File.recursive_overwrite( self.get_song_file(temp=True), self.get_song_file(temp=False) )
        File.recursive_overwrite( self.get_song_file(temp=True), self.get_song_file(version="original", temp=False) )
