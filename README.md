# LOF Song Manager
Compressing, sharing, and version controlling Studio One projects for Bands.

## Installation
You must have the following pre-installed:

 - Python 3.x and Pip
   - Mac: You can install using HomeBrew `brew install python`
   - Windows: https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe 
 - ffmpeg
   - Mac: You can install using HomeBrew, `brew install ffmpeg`
   - Windows: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
     - Extract the `ffmpeg` directory from the *.7z package
 - Git
   - Mac: You can install using HomeBrew, `brew install git`
   - Windows: https://github.com/git-for-windows/git/releases/download/v2.28.0.windows.1/PortableGit-2.28.0-64-bit.7z.exe
     - Extract the `PortableGit` directory from the *.7z package
 - Google Drive API Tools
   - After installing Python and Pip, run:
     `pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

Once you have all that installed, download this repository and extract it to a location of your choice (We would suggest your documents folder or desktop).

### Google Drive Auth
You must get a copy of your Google Drive API's `credentials.json` file to gain access to your Google Drive server.  If you do not know what this is or how to gain access to it, ask your Google Drive administrator for a copy of this.  If you do not have an admin, or you are the admin and setting this up for the first time, refer to the Google Drive API docs located here: https://developers.google.com/docs/api/quickstart/python.  Look for the blue button titled `Enable the Google Docs API`.  Once you download this JSON file, you will need to rename it `credentials.json` and place it in the root of the project, `LOFSongManager/`.

### Windows Only
Next, take the extracted `ffmpeg` directory you downloaded earlier and move it into the `LOFSongManager/src/` directory.  Make sure you can see all the files and folders in `LOFSongManager/src/ffmpeg/<all the files>`.  If you have all the files in `LOFSongManager/src/<all the files>` or `LOFSongManager/src/ffmpeg/ffmpeg/<all the files>`, the program will not run correctly.

Next, take the extracted `PortableGit` directory you downloaded earlier and move it into the same location, `LOFSongManager/src/`.  Make sure you can see all the files and folders in `LOFSongManager/src/PortableGit/<all the files>`.  If you have all the files in `LOFSongManager/src/<all the files>` or `LOFSongManager/src/PortableGit/PortableGit/<all the files>`, the program will not run correctly.

### Additional
There is a file under `LOFSongManager/src/env.py` that contains the paths and hash id's of the directories that your project will be working off of on your Google Drive.  If you are the administrator, you MUST change these paths and hash values to match your setup.

## Setting up a shortcut
Once you have finished installing the program, we will need to set up a shortcut so you can run this software easily.

 - Windows: 
 In file explorer, navigate to your program directory `LOFSongManager/` and right-click on the file `LOFSongManager.bat`.  Go to `Send to > Desktop (create shortcut)`.  This will provide you with a shortcut to your desktop for easy access.
 - Mac: In the finder, navigate to your program directory `LOFSongManager/` and right-click on the file `LOFSongManager.sh`.  Go to `Make Alias`.  Drag this new alias file to the desktop.  This will provide you with a shortcut to your desktop for easy access.

## First Time Running
When the software attempts to conenct to Google Drive for the first time, a browser window will pop up to confirm your credentials with the Google Drive API.  You must accept and allow these credentials in order for this program to work properly.  You can disable this app from accessing your account at any time by logging into your google account and disabling this app and these API credentials.

# How to Use
Coming Soon.
