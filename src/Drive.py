import os, io, pickle, shutil
from pathlib import Path
from src.File import File
from src.env import LOFSM_DIR_HASH
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Drive:
    mimeType = {
        "zip":    "application/x-gzip",
        "folder": "application/vnd.google-apps.folder",
        "json":   "application/json",
    }

    def __init__(self):
        self.service = None

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

        self.service = build("drive", "v3", credentials=creds)

    def get_info(self, search):
        if "/" in search:
            path_list = search.split("/")
            parent    = None

            for folder in path_list:
                results = self.ls(search="root" if not parent else parent)
                result  = next((x for x in results if x["name"] == folder), None)

                if not result:
                    return False

                parent = result["id"]

            return parent
        else:
            raise Exception("Drive.get_info requires a valid filepath!")

    def ls(self, search):
        if not search:
            raise Exception(f'Path: "{search}" doesn\'t exist!')

        if "/" in search:
            # The self.get_info will trigger the above exception if no file/folder is found
            return self.ls( self.get_info(search)["id"] )
        else:
            # If the search is a file/folder ID
            return self.service.files().list(q=f'"{search}" in parents and trashed=False').execute().get("files", [])

    def print_ls(self, ls):
        for result in ls:
            print(f' - Name: "{result["name"]}" | Id: "{result["id"]}"')

    def mkdir(self, name="Untitled", parents=[LOFSM_DIR_HASH]):
        return self.service.files().create(body={
            "name":     name,
            "mimeType": mimeType["folder"],
            "parents":  parents,
        }).execute()

    def upload(self, filepath, mimeType, parents=[LOFSM_DIR_HASH]):
        filepath = Path(filepath)
        file     = None

        # Check to see if the file is already uploaded
        results = self.ls(search=parents[0])
        for r in results:
            if r["name"] == filepath.name:
                # Update
                file = self.service.files().update(
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
            file = self.service.files().create(
                body={
                    "name":    filepath.name,
                    "parents": parents,
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
            print("Uploaded successfully!")
            return True
        else:
            print(f'Failed to upload "{filepath.name}"!')
            return False

    def download(self, ID, save_path):
        save_path  = Path(save_path)
        request    = self.service.files().get_media(fileId=ID)
        fh         = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request, chunksize=51200*1024)

        print(f"----> Downloaded 0%", end="\r", flush=True)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print(f"----> Downloaded {int(status.progress() * 100)}%", end="\r", flush=True)

        if downloader:
            print("Downloaded successfully!")

            fh.seek(0)
            with open(save_path.absolute(), "wb") as f:
                shutil.copyfileobj(fh, f, length=1024*1024)

            return True
        return False

    def get_json(self, remote_file, local_filepath):
        # remote_file    = cloud ID or cloud filepath
        # local_filepath = place to save the json file temporarily
        local_filepath = Path(local_filepath)

        download = self.download(
            ID        = self.get_info(remote_file),
            save_path = local_filepath
        )

        if not download:
            raise Exception(f'Something went wrong when downloading "{local_filepath.name}"')

        return File.get_json(local_filepath)

    def set_json(self, remote_file, local_filepath, parents=[LOFSM_DIR_HASH]):
        # remote_file    = cloud ID or cloud filepath
        # local_filepath = place to save the json file temporarily
        local_filepath = Path(local_filepath)

        upload = self.upload(
            filepath = local_filepath,
            mimeType = Drive.mimeType["json"],
            parents  = parents
        )

        if not upload:
            raise Exception(f'Something went wrong when uploading "{local_filepath.name}"')

    def get_json_key(self, remote_file, local_filepath, key):
        # remote_file    = cloud ID or cloud filepath
        # local_filepath = place to save the json file temporarily
        self.get_json(remote_file, local_filepath)
        return File.get_json_key(local_filepath, key)

    def set_json_key(self, remote_file, local_filepath, key, data, parents=[LOFSM_DIR_HASH]):
        self.get_json(remote_file, local_filepath)
        File.set_json_key(local_filepath, key, data)
        self.set_json(remote_file, local_filepath, parents)
