from glob import glob
from pathlib import Path
from src.TERMGUI.Run import Run
from src.TERMGUI.Log import Log
from src.TERMGUI.Dialog import Dialog
from src.DummyFiles import DummyFiles
from src.FileManagement.File import File
from src.FileManagement.Folder import Folder
from src.Settings import Settings


class Audio:
    def __init__(self, filepath):
        self.filepath = Path(filepath)

    def to_wav(self, folderpath):
        folderpath = Path(folderpath)
        Folder.create(folderpath)

        mp3            = self.filepath
        wav            = Path(f'{folderpath.absolute()}/{mp3.stem}.wav')
        dummy_files    = DummyFiles(folderpath)
        dummy_max      = 0
        dummy_list     = dummy_files.get_list()
        stem, num, ext = File.split_name(wav.name)

        if dummy_files.is_in_max(stem):
            dummy_max  = dummy_files.get_max()[stem]

        if wav.is_file() and num <= dummy_max and not wav.name in dummy_list:
            # File already exists locally, do not do anything
            Log(f'File "{wav.name}" already exists, keeping local file.')
            return True

        elif wav.is_file() and num > dummy_max:
            if dummy_max == 0:
                wav_old = Path(f'{folderpath.absolute()}/{stem}_old.{ext}')
            else:
                wav_old = Path(f'{folderpath.absolute()}/{stem}_old({num}).{ext}')

            Dialog(
                title = "Warning! Audio File Conflict Found!",
                body  = [
                    f'Because the audio file "{wav.name}" exists in your local',
                    f'project as well as the cloud project you are trying to',
                    f'download.. We need to figure out which one to keep!',
                    f'\n',
                    f'\n',
                    f'This software will take the current local version of',
                    f'"{wav.name}" and rename it to "{wav_old.name}".',
                    f'Then copy the new audio file into the pool.  You will have',
                    f'to go into the project and figure out which audio file is',
                    f'the correct one!',
                    f'\n',
                    f'\n',
                    f'Usually, this occurs when recording to the wrong track.',
                    f'Please make sure you only record to tracks that have your',
                    f'own name in them!',
                    f'\n',
                    f'\n',
                    f'You will have to either delete this *_old* file or rename',
                    f'it and re-link inside Studio One before you will be allowed',
                    f'to upload to the cloud again!',
                    f'\n',
                    f'\n',
                ],
                clear = False
            ).press_enter()

            if not wav_old.exists():
                File.recursive_overwrite(
                    src  = wav.absolute(),
                    dest = wav_old.absolute()
                )
                File.delete(wav)

            else:
                Dialog(
                    title = f'Error! "{wav_old.name}" Already Exists!',
                    body = [
                        f'The previous audio file conflict must be resolved',
                        f'before you can continue!',
                        f'\n',
                        f'\n',
                        f'To resolve this conflict, you must either rename the file',
                        f'\n',
                        f'\n',
                        f' - "{wav_old.absolute()}"',
                        f'\n',
                        f'\n',
                        f'to something else and re-link the newly',
                        f'renamed file inside Studio One, or delete this file!',
                        f'\n',
                        f'\n',
                    ],
                    clear = False
                ).press_enter()

                return False

        else:
            if wav.name in dummy_list:
                Dialog(
                    title = "Warning! Dummy File Conflict!",
                    body  = [
                        f'Audio file "{wav.name}" exists locally as a dummy file!',
                        f'This means that the last user that uploaded this project',
                        f'recorded over a dummy file.',
                        f'\n',
                        f'\n',
                        f'Even though no audio data has been lost, this could mean',
                        f'that a serious error has occurred and should be reported',
                        f'to your administrator.',
                        f'\n',
                        f'\n',
                    ],
                    clear = False
                ).press_enter()

        Run.ffmpeg(
            args        = "-i",
            source      = mp3.absolute(),
            destination = wav.absolute(),
            codec       = "-c:a pcm_s24le"
        )
        return True

    def to_mp3(self, folderpath, username_ignore=False):
        folderpath = Path(folderpath)

        wav         = self.filepath
        mp3         = Path(f'{folderpath.absolute()}/{wav.stem}.mp3')
        dummy_files = DummyFiles(wav.parent)
        username    = Settings.get_username()

        if "_old" in wav.name:
            Dialog(
                title = "Warning! Can't Upload *_old* Audio File!",
                body  = [
                    f'It appears that you have not yet resolved the audio file',
                    f'conflict for "{wav.name}"!  You must either delete this file,',
                    f'or re-name it and re-link it in Studio One!',
                    f'\n',
                    f'\n',
                ],
                clear = False
            ).press_enter()
            return False

        if wav.name in dummy_files.get_list():
            return True

        if not mp3.is_file():
            if not username in wav.name.lower() and not username_ignore:
                dialog = Dialog(
                    title = "Warning! Where Is Your Name?!",
                    body  = [
                        f'It appears that the file',
                        f'\n',
                        f'\n',
                        f' - {wav.parent.absolute().name}/{wav.name}',
                        f'\n',
                        f'\n',
                        f'does not contain your name.. Are you sure you recorded',
                        f'on the correct track?!  Doing this can cause serious',
                        f'version control issues!!',
                        f'\n',
                        f'\n',
                        f'Since you have already removed unused audio files from',
                        f'the pool, AND selected the checkbox to delete those',
                        f'audio files..  You should go back into your Studio One',
                        f'project, remove this clip from the timeline, OR rename',
                        f'this clip to include your name, and then re-run the',
                        f'upload!',
                        f'\n',
                        f'\n',
                        f'If you are ABSOLUTELY SURE that this is in error, aka',
                        f'uploading a project from band practice, then type "yes"',
                        f'at the prompt, or "yesall" to ignore all other warnings',
                        f'for this.',
                        f'\n',
                        f'\n',
                        f'If you want to exit now, type "no" at the prompt.',
                        f'\n',
                        f'\n',
                    ],
                    clear = False
                )
                ans = dialog.get_mult_choice(["yes", "yesall", "no"])

                if ans == "no":
                    return False
                elif ans == "yesall":
                    username_ignore = True

        else:
            Log(f'Keeping cached file "{mp3.name}"')
            return True

        Run.ffmpeg(
            args        = "-i",
            source      = wav.absolute(),
            destination = mp3.absolute(),
            codec       = ""
        )

        if username_ignore:
            return {"username_ignore": True}
        return True

    def folder_to_mp3(folderpath, destination):
        folderpath      = Path(folderpath)
        destination     = Path(destination)
        wavs            = glob(f"{folderpath.absolute()}/*.wav")
        username_ignore = False

        Folder.create(destination)

        for wav in wavs:
            result = Audio(wav).to_mp3(
                folderpath      = destination,
                username_ignore = username_ignore
            )

            if isinstance(result, dict):
                username_ignore = result["username_ignore"]
            else:
                if not result:
                    return False

        return True

    def folder_to_wav(folderpath, destination):
        folderpath  = Path(folderpath)
        destination = Path(destination)
        mp3s        = glob(f"{folderpath.absolute()}/*.mp3")

        for mp3 in mp3s:
            if not Audio(mp3).to_wav(destination):
                return False
        return True

