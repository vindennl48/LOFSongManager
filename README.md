# ![Repository of Fires](./assets/black-circle.png) LOF Song Manager

Compressing, sharing, and version controlling Studio One projects for bands.

## Installation

This project is designed to work with [Studio One]. Additionally, there are a
few packages that must be manually installed using the Terminal or Command
Prompt. At times, you'll need to find a file that you just downloaded, or run a
command in a specific directory.

[Studio One]: https://en.wikipedia.org/wiki/Studio_One_(software)

---

### Mac

Most people reading this will already be familiar with [Homebrew], which is far
and away the easiest way to install the dependencies.

```
$ brew install python ffmpeg git
```

Next, clone the project.

```
$ git clone https://github.com/vindennl48/LOFSongManager.git
```

Last, install the required Python packages from the project directory.

```
$ pip3 install -r requirements.txt
````

[Homebrew]: https://brew.sh/

---

### Windows

If you follow these instructions, you'll find that the FFmpeg and Git downloads
have a `.7z` extension. These files are [7-zip] archives, which need to be
extracted after they are downloaded (similar to Zip files) using the 7-zip
utility.

[7-zip]: https://www.7-zip.org/

#### Python 3 and pip

The [Python downloads page] is the quickest way to get the most recent version
of Python 3 (and pip, which is included with Python). Past Python releases are
[available for download] as well.

[Python downloads page]: https://www.python.org/downloads/
[available for download]: https://www.python.org/ftp/python/

#### FFmpeg

The official [FFmpeg site] doesn't host any compiled builds of FFmpeg (source
code only). However, you can click through to [gyan.dev], where builds of FFmpeg
are already compiled for Windows and ready to download.

Click [here] to begin downloading the most recent release of FFmpeg. Once
downloaded, extract FFmpeg from the 7-zip archive, and keep it handy for the
next step.

[FFmpeg site]: https://ffmpeg.org/download.html#build-windows
[gyan.dev]: https://www.gyan.dev/ffmpeg/builds/
[here]: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z

#### Git

The [Git downloads page for Windows] has a few different builds available for
download, but this project specifically requires the portable version.

Go to the downloads page. Find the link, "64-bit Git for Windows Portable".
Click the link to begin downloading the most recent version of PortableGit. Once
downloaded, extract PortableGit from the 7-zip archive, and keep it handy for
the next step.

[Git downloads page for Windows]: https://git-scm.com/download/win

#### Finish installing

Once you have all that installed, clone this repository. Then, enter the
project directory using the Command Prompt, and install the required Python
packages.

```
C:\> pip3 install -r requirements.txt
````

---

### Google Drive Auth

You must get a copy of your Google Drive API's `credentials.json` file to gain
access to your Google Drive server. If you do not know what this is or how to
gain access to it, ask your Google Drive administrator for a copy of this. If
you do not have an admin, or you are the admin and setting this up for the first
time, refer to the Google Drive API docs located here:
https://developers.google.com/docs/api/quickstart/python. Look for the blue
button titled `Enable the Google Docs API`. Once you download this JSON file,
you will need to rename it `credentials.json` and place it in the root of the
project, `LOFSongManager/`.

### Windows Only

Next, take the extracted `ffmpeg` directory you downloaded earlier and move it
into the `LOFSongManager/src/` directory. Make sure you can see all the files
and folders in `LOFSongManager/src/ffmpeg/<all the files>`. If you have all the
files in `LOFSongManager/src/<all the files>` or
`LOFSongManager/src/ffmpeg/ffmpeg/<all the files>`, the program will not run
correctly.

Next, take the extracted `PortableGit` directory you downloaded earlier and move
it into the same location, `LOFSongManager/src/`. Make sure you can see all the
files and folders in `LOFSongManager/src/PortableGit/<all the files>`. If you
have all the files in `LOFSongManager/src/<all the files>` or
`LOFSongManager/src/PortableGit/PortableGit/<all the files>`, the program will
not run correctly.

### Additional

There is a file under `LOFSongManager/src/env.py` that contains the paths and
hash id's of the directories that your project will be working off of on your
Google Drive. If you are the administrator, you MUST change these paths and
hash values to match your setup.

## Setting up a shortcut

Once you have finished installing the program, we will need to set up a shortcut
so you can run this software easily.

- Windows: In file explorer, navigate to your program directory
  `LOFSongManager/` and right-click on the file `LOFSongManager.bat`. Go to
  `Send to > Desktop (create shortcut)`. This will provide you with a shortcut
  to your desktop for easy access.
- Mac: In the finder, navigate to your program directory `LOFSongManager/` and
  right-click on the file `LOFSongManager.sh`. Go to `Make Alias`. Drag this
  new alias file to the desktop. This will provide you with a shortcut to your
  desktop for easy access.

## First Time Running

When the software attempts to connect to Google Drive for the first time, a
browser window will pop up to confirm your credentials with the Google Drive
API. You must accept and allow these credentials in order for this program to
work properly. You can disable this app from accessing your account at any time
by logging into your google account and disabling this app and these API
credentials.

# How to Use

Coming Soon.
