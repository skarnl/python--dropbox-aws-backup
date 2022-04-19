import os
import pickle

HISTORY_FILE = ".__history.cfg"


def get_history():
    with open(HISTORY_FILE, "rb") as fp:
        return pickle.load(fp)


def add_to_history(folder):
    history_list = get_history()
    history_list.append(folder)

    with open(HISTORY_FILE, "wb") as fp:
        pickle.dump(history_list, fp)


def write_file():
    with open(HISTORY_FILE, "wb") as fp:
        pickle.dump([], fp)


if not os.path.isfile(HISTORY_FILE):
    write_file()
