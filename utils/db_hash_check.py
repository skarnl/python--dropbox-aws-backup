from utils.dropbox_content_hasher import DropboxContentHasher


def get_file_hash(file_path):
    hasher = DropboxContentHasher()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(1024)  # or whatever chunk size you want
            if len(chunk) == 0:
                break
            hasher.update(chunk)
    return hasher.hexdigest()
