import os
import pickle
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Drive:
    mimeType = {
        'zip':    'application/x-gzip',
        'folder': 'application/vnd.google-apps.folder',
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

    def get_info(self, path=None, trashed=False):
        if path:
            path_list = path.split('/')

            parent = None
            result = None
            for folder in path_list:
                results = self.ls(search='root' if not parent else parent)
                result  = next((x for x in results if x['name'] == folder), None)
                if not result:
                    raise Exception(f"Path: '{path}' doesn't exist!")
                parent = result['id']

            return result

        else:
            raise Exception("Drive.get_info(): Need path!")

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
                chunksize=1024*1024,
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


if __name__ == "__main__":
    drive = Drive()

    # items = drive.ls(id='1DEMYiL1aiRJYjf_B3QyKkUbow4xqNaJQ')
    parent = drive.get_info(path='Land of Fires/Audio/LOFSongManager')

    drive.upload_progress(
        file     = './compressed_songs/Pemi.lof',
        mimeType = Drive.mimeType['zip'],
        parents  = [parent['id']]
    )
