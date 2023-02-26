import os
import pandas as pd

from typing import Union


class ReadObject(object):
    def __init__(self, host: str, ports: Union[str, None]):
        self.host = host
        self._ports = ports
        self._results = []

    @property
    def ports(self):
        if self._results:
            return self._results
        self._results = [int(port) for port in self._ports.split(",")]
        return self._results

    def __repr__(self) -> str:
        return "ReadObject({0}, {1})".format(self.host, self.ports)


class CSVReader(object):
    def __init__(self, filename: str):
        self.filename = filename
        self.input_error_status = False

        self.units = self.read()

    def get_file_exists_status(self) -> bool:
        return os.path.exists(self.filename)

    def read(self):
        if self.get_file_exists_status():
            data = pd.read_csv(self.filename, sep=";")
            values = []
            for host, ports in data.values.tolist():
                if ports == "nan":
                    ports = None
                if host == "nan":
                    host = None
                if not ports.isdigit():
                    self.input_error_status = True
                values.append(ReadObject(host, ports))
            return values
        return []

    def __repr__(self) -> str:
        return "CSVReader({0})".format(self.filename)

    def __str__(self):
        return "[{0}]".format(", ".join([repr(obj) for obj in self.units]))

    def __call__(self):
        yield from self.units
