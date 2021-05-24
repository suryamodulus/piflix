from os import makedirs, path
import pathlib

def check_media_folder_path(folder_path):
    if(folder_path and path.exists(folder_path) and path.isdir(folder_path)):
        return
    raise Exception('Invalid MEDIA_FOLDER_PATH check config.py')


def check_allowed_extensions(filename, allowed_media_extensions):
    file_extension = pathlib.Path(filename).suffix
    if(file_extension and (file_extension in allowed_media_extensions)):
        return
    else:
        raise Exception(f'File with extension {file_extension} not allowed')