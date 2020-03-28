from pathlib import Path

FILES_DIR = "files"


def get_files_dir():
    return Path(__file__).parent.joinpath(FILES_DIR)


def load_file(filename):
    file_path = str(get_files_dir().joinpath(filename))
    with open(file_path, "r") as f:
        return f.read()
