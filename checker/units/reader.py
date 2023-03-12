# -*- coding:utf-8 -*-
"""
The MIT License (MIT)
Copyright (c) 2023-present Dmitry Filinov (D1ffic00lt)
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import os
import pandas as pd

from typing import Union, Generator

from checker.units.exceptions import DataInvalidFormat, FileInvalidFormat


__all__ = (
    "ReadObject", "CSVReader"
)

class ReadObject(object):
    r"""
    A single site-object for which checks will be carried out

    host: str
        Website host (IP or domain name)
    ports: list[int]
        Site port or ports
    """
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
    """
    Class for reading and processing data from a .csv file

    get_file_exists_status() -> bool
        Checks for the existence of a .csv file
    read() -> list[ReadObject]
        Reads .csv file and performs necessary checks
    __call__(self) -> Generator
        Returns a generator from ReadObject objects
    """
    __slots__ = (
        "filename", "input_error_status", "units"
    )
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.input_error_status = False

        self.units = self.read()

    def get_file_exists_status(self) -> bool:
        r"""
        Checks for the existence of a .csv file

        Returns
        --------
           Returns the presence status of a file
        """
        return os.path.isfile(self.filename)

    def read(self) -> list[ReadObject]:
        r"""
        Reads .csv file and performs necessary checks

        Returns
        --------
           List of sites from .csv file (list[ReadObject])
        """
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
        r"""
        Returns a generator from ReadObject objects

        Returns
        --------
           A generator from ReadObject objects
        """
        yield from self.units
