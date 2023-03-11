# -*- coding:utf-8 -*-
import os
import pandas as pd

from typing import Union, Generator

from checker.units.exceptions import DataInvalidFormat, FileInvalidFormat


__all__ = (
    "ReadObject", "CSVReader"
)

class ReadObject(object):
    __slots__ = (
        "host", "_ports", "_results"
    )
    def __init__(self, host: str, ports: Union[str, None]) -> None:
        self.host = host
        self._ports = ports

        if ports == "" or ports is None:
            self._ports = ""

        self._results = []

    @property
    def ports(self) -> list[int]:
        if self._results or self._ports == "":
            return self._results

        self._results = [int(port) for port in self._ports.split(",")]
        return self._results

    def __repr__(self) -> str:
        return "{0}({1}, {2})".format(self.__class__.__name__, self.host, self.ports)


class CSVReader(object):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.input_error_status = False

        self.units = self.read()

    def get_file_exists_status(self) -> bool:
        return os.path.isfile(self.filename)

    def read(self) -> list[ReadObject]:
        if not self.get_file_exists_status():
            self.input_error_status = FileInvalidFormat("file {0} not found".format(self.filename))
            return []

        try:
            if self.filename[-4:] != ".csv":
                self.input_error_status = FileInvalidFormat("file {0} must be .csv".format(self.filename))
                return []
        except IndexError:
            self.input_error_status = FileInvalidFormat("the total filename length must be >= 4 characters")
            return []
        except Exception as e:
            self.input_error_status = FileInvalidFormat(e.args[0] + f"{e.__class__.__name__}")
            return []

        data = pd.read_csv(self.filename, sep=";")

        if list(map(str.lower, data.columns)) != ["host", "ports"]:
            self.input_error_status = FileInvalidFormat("the table should have columns \"Host\" and \"Ports\"")
            return []

        data = data.astype(str)
        values = []

        for host, ports in data.values.tolist():
            if ports in ["nan", "", [], None]:
                ports = None
            else:
                if not ports.isdigit():
                    if not all([i.isdigit() for i in ports.split(",")]):
                        self.input_error_status = DataInvalidFormat("all ports must be int ({0})".format(ports))
                        continue

            if host in ["nan", "", [], None]:
                host = None
                self.input_error_status = DataInvalidFormat("host must be not None")

            values.append(ReadObject(host, ports))
        return values

    def __repr__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, self.filename)

    def __str__(self) -> str:
        return "[{0}]".format(", ".join([repr(obj) for obj in self.units]))

    def __call__(self) -> Generator:
        yield from self.units
