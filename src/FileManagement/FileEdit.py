from pathlib import Path

class FileEdit:
    def append(filepath, text):
        filepath = Path(filepath)

        with open(filepath.absolute(), "a") as f:
            f.write(f'{text}\n')

    def delete(filepath):
        filepath = Path(filepath)

        if filepath.exists():
            filepath.unlink()

