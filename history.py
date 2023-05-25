import os
import pickle

HISTORY_FILE_POSTFIX = "__history.cache"

class History:

    _file_name = ''

    def __init__(self, name):
        self._file_name = f'.{name}{HISTORY_FILE_POSTFIX}'

        if not os.path.isfile(self._file_name):
            print(f"History::__init__ : Create file {self._file_name}")

            self.write_file()


    def get_history(self):
        with open(self._file_name, "rb") as fp:
            return pickle.load(fp)


    def add_to_history(self, folder):
        history_list = self.get_history()
        history_list.append(folder)

        with open(self._file_name, "wb") as fp:
            pickle.dump(history_list, fp)


    def write_file(self):
        with open(self._file_name, "wb") as fp:
            pickle.dump([], fp)


    def reset(self):
        print(f"History :: Reset history cache : {self._file_name}")
        self.write_file()

