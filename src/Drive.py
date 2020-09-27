import os
import io
import pickle
import shutil
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Drive:
    mimeType = {
        'zip':    'application/x-gzip',
        'folder': 'application/vnd.google-apps.folder',
        'json':   'application/json',
    }

    def __init__(self):
        self.service = None

        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive']
        # SCOPES = ['https://www.googleapis.com/auth/admin.directory.group']
        creds  = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

    def ls(self, path=None, search=None, trashed=False):
        if not path and not search:
            raise Exception("Drive.ls():  Need to provide a search query!")

        if path:
            path_list = path.split('/')

            parent = None
            for folder in path_list:
                results = self.ls(search='root' if not parent else parent)
                result  = next((x for x in results if x['name'] == folder), None)
                if not result:
                    raise Exception(f"Path: '{path}' doesn't exist!")
                parent = result['id']

            return self.ls(search=parent)

        else:
            return self.service.files().list(q=f"'{search}' in parents and trashed={trashed}").execute().get('files', [])

    def print_ls(self, leader="", search=None, array=None, trashed=False):
        if array:
            results = array
        else:
            results = self.ls(search=search)

        for result in results:
            print(f"{leader}Name: '{result['name']}' | Id: '{result['id']}'")

    def get_info(self, id=None, path=None, trashed=False):
        if id:
            result = self.ls(search=id)
            if not result:
                return False
            return result

        elif path:
            path_list = path.split('/')

            parent = None
            result = None
            for folder in path_list:
                results = self.ls(search='root' if not parent else parent)
                result  = next((x for x in results if x['name'] == folder), None)
                if not result:
                    return False
                    # raise Exception(f"Path: '{path}' doesn't exist!")
                parent = result['id']

            return result

        else:
            raise Exception("Drive.get_info(): Need id or path!")

    def mkdir(self, name='Untitled', parents=['root']):
        return self.service.files().create(body={
            'name':     name,
            'mimeType': mimeType['folder'],
            'parents':  parents,
        }).execute()

    def upload(self, file, mimeType, parents=['root']):
        file = Path(file)

        file = self.service.files().create(
            body={
                'name':    file.name,
                'parents': parents,
            },
            media_body=MediaFileUpload(
                file.absolute(),
                chunksize=51200*1024,
                mimetype=mimeType,
                resumable=True
            )
        )

        response = None
        while response is None:
            status, response = file.next_chunk()
            if status:
                print(f"----> Uploaded {int(status.progress() * 100)}%", end="\r", flush=True)

        if file:
            print("Uploaded successfully!")

    def update(self, file, mimeType, drive_file_id):
        file = Path(file)

        file = self.service.files().update(
            fileId=drive_file_id,
            body={
                'name': file.name,
            },
            media_body=MediaFileUpload(
                file.absolute(),
                chunksize=51200*1024,
                mimetype=mimeType,
                resumable=True
            )
        )

        response = None
        while response is None:
            status, response = file.next_chunk()
            if status:
                print(f"----> Uploaded {int(status.progress() * 100)}%", end="\r", flush=True)

        if file:
            print("Uploaded successfully!")

    def download(self, id=None, save_path=None):
        if not id or not save_path:
            raise Exception('Drive.download():  Need file ID and save path!')

        save_path  = Path(save_path)
        request    = self.service.files().get_media(fileId=id)
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
            with open(save_path.absolute(), 'wb') as f:
                shutil.copyfileobj(fh, f, length=1024*1024)

            return True
        return False


# from src.helpers import *

# if __name__ == "__main__":
    # drive = Drive()

    # compare_hash(drive, 'Pemi.lof')

    # # items = drive.ls(id='1DEMYiL1aiRJYjf_B3QyKkUbow4xqNaJQ')
    # parent = drive.get_info(path='Land of Fires/Audio/LOFSongManager')

    # drive.upload_progress(
        # file     = './compressed_songs/Pemi.lof',
        # mimeType = Drive.mimeType['zip'],
        # parents  = [parent['id']]
    # )
