import re
import socket
import requests

from ping3 import ping
from datetime import datetime

from exceptions import IgnoreInternetExceptions
from reader import ReadObject
from config import IP


class Checker(object):
    def __init__(self, data: ReadObject):
        self.data: ReadObject = data

    def __repr__(self):
        return "Checker({0})".format(repr(self.data))

    @staticmethod
    @IgnoreInternetExceptions(check_ip=True)
    def get_ip_success(ip: str) -> requests.models.Response:
        return requests.get(f"http://{ip}" if "http" not in ip else ip, timeout=10)

    @staticmethod
    def check_port(host: str, port: int):
        socket_connection = socket.socket()
        try:
            socket_connection.connect((host, port))
        except (socket.gaierror, ConnectionRefusedError):
            return False
        return True

    @staticmethod
    def get_ip_from_host(host: str):
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            return False

    @IgnoreInternetExceptions()
    def __call__(self):
        if self.data.host is not None:
            is_ip = re.findall(IP, self.data.host) != []
            if is_ip:
                ip = ".".join(re.findall(IP, self.data.host)[0])
                if not self.get_ip_success(ip):
                    return "ip is not success"
                if not self.check_port(ip, 443) or not self.check_port(ip, 80):
                    return "HTTPS or HTT ports closed"
                if self.get_ip_success(ip).status_code // 100 not in [1, 2, 3]:
                    return "bad request code ({0})".format(self.get_ip_success(ip).status_code)
            else:
                if self.data.ports is not None:
                    if not self.check_port(self.data.host, 443) or not self.check_port(self.data.host, 80):
                        return "HTTPS or HTT ports closed"
                if isinstance(self.get_ip_from_host(self.data.host), bool):
                    return "cant get ip from the host ({0})".format(self.data.host)
                if not self.get_ip_success(self.data.host):
                    return "ip is not success"
                if self.get_ip_success(self.data.host).status_code // 100 not in [1, 2, 3]:
                    return "bad request code ({0})".format(self.get_ip_success(self.data.host).status_code)

            host_display_name = "???" if is_ip else self.data.host
            host_ip = self.get_ip_from_host(self.data.host)
            host_ip = [host_ip] if isinstance(host_ip, str) else host_ip

            if self.data.ports is None:
                return [host_display_name, host_ip, self.data.ports], \
                    "{0} | {1} | {2} | {3} | {4:.3} ms | -1 | ???".format(
                        datetime.now(), host_display_name, host_ip, 0.0,
                        ping(host_ip, timeout=500, unit="ms")
                    )
            else:
                result = ""
                for ip in host_ip:
                    for port in self.data.ports:
                        result += "{0} | {1} | {2} | 0.0 | {3:.3} ms | {4} | {5}\n".format(
                            datetime.now(), host_display_name, ip,
                            ping(ip, timeout=500, unit="ms"), port,
                            "Opened" if self.check_port(ip, port) else "Not opened"
                        )
                return result


if __name__ == "__main__":
    print(Checker(ReadObject("localhost", ""))())
