import os

CACHE_FILE = ".__dropbox_auth.cache"


def get_cached_token():
    with open(CACHE_FILE, "r") as fp:
        token = fp.read()
        return None if token == "" else token


def store_token_in_cache(token):
    with open(CACHE_FILE, "w") as fp:
        fp.write(token)


if not os.path.isfile(CACHE_FILE):
    store_token_in_cache("")
