import os, io, pickle, shutil
from pathlib import Path
from src.dev import Dev
from src.TERMGUI.Log import Log
from src.Settings import Settings
from src.TERMGUI.Dialog import Dialog
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Definitions
KEY_CLOUD_ROOT_ID     = "cloud_root_id"
KEY_CLOUD_ROOT_ID_DEV = "cloud_root_id_dev"


class Drive:
    service = None
    root_id = None

    mimeType = {
        "zip":    "application/x-gzip",
        "folder": "application/vnd.google-apps.folder",
        "json":   "application/json",
        "mp3":    "audio/mp3",
    }

    def initialize():
        Drive.service = None

        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        # SCOPES = ["https://www.googleapis.com/auth/admin.directory.group"]
        creds  = None

        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        Drive.service = build("drive", "v3", credentials=creds)

        # Root of the LOFSM project on the cloud
        Drive.root_id = Drive.get_root_id()

    def get_root_id():
        # Check to see which root id we are getting
        key   = KEY_CLOUD_ROOT_ID
        title = "Cloud ID Missing"
        if Dev.get("ALT_LOCATION"):
            key   = KEY_CLOUD_ROOT_ID_DEV
            title = "Cloud DEVELOPMENT ID Missing"

        # Get the ID from Settings
        result = Settings.get_key(key)

        # If the ID doesnt exist in settings, lets ask for it!
        if not result:
            dialog = Dialog(
                title = title,
                body  = [
                    f'The Cloud root ID is currently missing.. So lets find it!',
                    f'\n',
                    f'\n',
                    f'Ask your administrator for the "Cloud Root Filepath" and',
                    f'enter that path below.',
                    f'\n',
                    f'\n',
                ]
            )
            ans = dialog.get_result("Filepath")

            result = Drive.get_id(search=ans, root="root")

            if not result:
                raise Exception("There was a problem with getting the Cloud Root ID..")

            Settings.set_key(key, result)

        return result

    def get_id(search=None, root=None):
        # This function lets you get the ID of a file / folder
        # search = file / folder path
        # root   = id of root, starting point for search path

        # If there is no value for 'root', set root to project root
        if not root:
            root = Drive.root_id

        # If there is no value for 'search', the root_id is returned
        # Provides an easy way of getting the project root_id
        if not search:
            return root

        path_list = search.split("/")
        parent    = None

        for folder in path_list:
            results = Drive.ls(search=root if not parent else parent)
            result  = next((x for x in results if x["name"] == folder), None)

            if not result:
                return None

            parent = result["id"]

        # Because of the recursive nature of this function, 'parent'
        #  ends up being the requested file/folder at the end.
        return parent

    def ls(search=None, filter=None):
        # Search can only be either Path or ID
        # To LS into directory in project root do:
        #   Drive.ls(search=Drive.get_id("<folder>"))

        # filter is a mimeType to sort out different filetypes
        # example:
        #   Drive.ls(search=Drive.root_id, filter=Drive.mimeType["zip"])
        result = None

        if not search:
            result = Drive.ls( Drive.root_id )

        elif "/" in search:
            # If the search term is a path
            result = Drive.ls( Drive.get_id(search) )
        else:
            # If the search term is a folder ID
            result = Drive.service.files().list(q=f'"{search}" in parents and trashed=False').execute().get("files", [])

        if filter:
            return [ x for x in result if x["mimeType"] == filter ]
        return result

    def print_ls(ls):
        for result in ls:
            print(f' - Name: "{result["name"]}" | Id: "{result["id"]}"')

    def mkdir(name="Untitled", parent=None):
        # Create folder inside parent directory
        # This returns the newly created folder ID

        # If no parent is specified, use the project root_id
        if not parent:
            parent = Drive.root_id

        # Check to make sure file doesn't already exist
        dir_id = Drive.get_id(name, parent)
        if dir_id:
            return dir_id

        return Drive.service.files().create(body={
            "name":     name,
            "mimeType": Drive.mimeType["folder"],
            "parents":  [ parent ],
        }).execute()["id"]

    def upload(filepath, mimeType, parent=None):

        # If no parent is specified, use the project root_id
        if not parent:
            parent = Drive.root_id

        if Dev.get("NO_UPLOAD"):
            Log("Dev Mode prevented 'Drive.upload' function","notice")
            return True

        filepath = Path(filepath)
        file     = None

        # Check to see if the file is already uploaded
        results = Drive.ls(parent)
        for r in results:
            if r["name"] == filepath.name:
                # Update
                file = Drive.service.files().update(
                    fileId=r["id"],
                    body={
                        "name": r["name"],
                    },
                    media_body=MediaFileUpload(
                        filepath.absolute(),
                        chunksize=51200*1024,
                        mimetype=mimeType,
                        resumable=True
                    )
                )
                break

        # If file is not already uploaded
        if not file:
            file = Drive.service.files().create(
                body={
                    "name":    filepath.name,
                    "parents": [ parent ],
                },
                media_body=MediaFileUpload(
                    filepath.absolute(),
                    chunksize=51200*1024,
                    mimetype=mimeType,
                    resumable=True
                )
            )

        # Upload
        print(f"----> Uploaded 0%", end="\r", flush=True)

        response = None
        while response is None:
            status, response = file.next_chunk()
            if status:
                print(f"----> Uploaded {int(status.progress() * 100)}%", end="\r", flush=True)

        if file:
            print("      Uploaded successfully!")
            return Drive.get_id(filepath.name, root=parent)
        else:
            print(f'Failed to upload "{filepath.name}"!')
            return False

    def download(ID, save_path):
        if Dev.get("NO_DOWNLOAD"):
            Log("Dev Mode prevented 'Drive.download' function","notice")
            return True

        save_path  = Path(save_path)
        request    = Drive.service.files().get_media(fileId=ID)
        fh         = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request, chunksize=51200*1024)

        print(f"----> Downloaded 0%", end="\r", flush=True)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print(f"----> Downloaded {int(status.progress() * 100)}%", end="\r", flush=True)

        if downloader:
            print("      Downloaded successfully!")

            fh.seek(0)
            with open(save_path.absolute(), "wb") as f:
                shutil.copyfileobj(fh, f, length=1024*1024)

            return True
        return False

    def delete(ID):
        result = Drive.service.files().delete(
            fileId = ID
        ).execute()

Drive.initialize()

#    These functions were part of the slowdown issue
################################################################################
#    def get_json(self, remote_file, local_filepath):
#        # remote_file    = cloud ID or cloud filepath
#        # local_filepath = place to save the json file temporarily
#        local_filepath = Path(local_filepath)
#
#        download = self.download(
#            ID        = self.get_info(remote_file),
#            save_path = local_filepath
#        )
#
#        if not download:
#            raise Exception(f'Something went wrong when downloading "{local_filepath.name}"')
#
#        return File.get_json(local_filepath)
#
#    def set_json(self, local_filepath, parent=None):
#        # remote_file    = cloud ID or cloud filepath
#        # local_filepath = place to save the json file temporarily
#
#        # If no parent is specified, use the project root_id
#        if not parent:
#            parent = self.root_id
#
#        local_filepath = Path(local_filepath)
#
#        upload = self.upload(
#            filepath = local_filepath,
#            mimeType = Drive.mimeType["json"],
#            parent   = parent
#        )
#
#        if not upload:
#            raise Exception(f'Something went wrong when uploading "{local_filepath.name}"')
#
#    def get_json_key(self, remote_file, local_filepath, key):
#        # remote_file    = cloud ID or cloud filepath
#        # local_filepath = place to save the json file temporarily
#        self.get_json(remote_file, local_filepath)
#        return File.get_json_key(local_filepath, key)
#
#    def set_json_key(self, remote_file, local_filepath, key, data, parent=None):
#        # If no parent is specified, use the project root_id
#        if not parent:
#            parent = self.root_id
#
#        self.get_json(remote_file, local_filepath)
#        File.set_json_key(local_filepath, key, data)
#        self.set_json(local_filepath, parent)
#
#    def remove_json_key(self, remote_file, local_filepath, key, parent=None):
#        # If no parent is specified, use the project root_id
#        if not parent:
#            parent = self.root_id
#
#        self.get_json(remote_file, local_filepath)
#        File.remove_json_key(local_filepath, key)
#        self.set_json(local_filepath, parent)
#
