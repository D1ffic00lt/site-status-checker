import os
import pandas as pd


class ReadObject(object):
    def __init__(self, host: str, ports: str):
        self.host = host
        self._ports = ports

    def get_request_type(self):
        pass

    @property
    def ports(self):
        if self._ports == "nan":
            return None
        result = []
        for port in self._ports.split(","):
            if port.isdigit():
                if float(port) == int(port):
                    result.append(int(port))
                else:
                    return AttributeError("Port must be int")
            else:
                return AttributeError("Port must be digit")

        return result

    def __repr__(self) -> str:
        return "ReadObject({0}, {1})".format(self.host, self.ports)


class CSVReader(object):
    def __init__(self, filename: str):
        self.filename = filename
        self.units = self.read()

    def get_file_exists_status(self) -> bool:
        return os.path.exists(self.filename)

    def read(self):
        if self.get_file_exists_status():
            data = pd.read_csv(self.filename, sep=";")
            return [ReadObject(host, ports) for host, ports in data.values.tolist()]
        return []

    def __repr__(self) -> str:
        return "CSVReader({0})".format(self.filename)

    def __str__(self):
        return "[{0}]".format(", ".join([repr(obj) for obj in self.units]))

    def __call__(self):
        yield from self.units
