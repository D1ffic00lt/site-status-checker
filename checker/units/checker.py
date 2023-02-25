from typing import List

from reader import CSVReader


class Checker(object):
    def __init__(self):
        self.data: List[CSVReader] = []

    def load(self, reader: CSVReader):
        self.data.append(reader)

    def __repr__(self):
        return "Checker()"
