import dropbox
import os
from tqdm import tqdm
from utils.db_hash_check import get_file_hash


def get_local_path(file_path, download_dir, folder_path):
    return remove_suffix(download_dir, "/") + remove_prefix(file_path, folder_path)


def make_should_download(download_dir, folder_path):
    def _should_download(entry):
        local_file_path = get_local_path(entry.path_lower, download_dir, folder_path)
        if os.path.exists(local_file_path):
            return get_file_hash(local_file_path) != entry.content_hash

        return True

    return _should_download


def get_files(dbx, folder_path, download_dir):
    result = dbx.files_list_folder(folder_path, recursive=True)

    file_list = []

    should_download = make_should_download(download_dir, folder_path)

    def process_entries(entries):
        for entry in entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                if should_download(entry):
                    file_list.append(entry.path_lower)

    process_entries(result.entries)

    while result.has_more and len(file_list) < 30:
        result = dbx.files_list_folder_continue(result.cursor)

        process_entries(result.entries)

    file_list = file_list[0:20]

    print("Downloading " + str(len(file_list)) + " files...")

    for fn in tqdm(file_list):
        local_file_path = get_local_path(fn, download_dir, folder_path)
        try:
            os.makedirs(os.path.dirname(os.path.abspath(local_file_path)))
        except:
            1 + 1

        dbx.files_download_to_file(local_file_path, fn)


# inspired by https://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string and
# https://stackoverflow.com/questions/1038824/how-do-i-remove-a-substring-from-the-end-of-a-string-in-python


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix) :]


def remove_suffix(text, suffix):
    return text[: -(text.endswith(suffix) and len(suffix))]
