import os


class Reader(object):
    def __init__(self, filename: str):
        self.filename = filename

    def get_file_exists_status(self):
        return os.path.exists(self.filename)

    def __repr__(self):
        return "{0}({1})".format(self.__module__, self.filename)
