import re
import socket
import requests
import urllib.error
import urllib.request

from ping3 import ping
from datetime import datetime

from checker.units.exceptions import IgnoreInternetExceptions, CheckerException, InternetConnectionError
from checker.units.reader import ReadObject
from checker.units.config import IP
from checker.units.config import headers

class Controller(object):
    def __init__(self, data: ReadObject):
        self.data: ReadObject = data

    @staticmethod
    @IgnoreInternetExceptions()
    def get_correct_url(url: str):
        if "http://" in url or "https://" in url:
            return url
        return "http://" + url

    @IgnoreInternetExceptions(check_ip=True)
    def get_ip_success(self, ip: str):
        try:
            requests.get(
                self.get_correct_url(ip), timeout=10,
                headers=headers
            )
        except requests.exceptions.Timeout:
            return False
        return True

    @IgnoreInternetExceptions()
    def get_status_code(self, url):
        try:
            conn = urllib.request.urlopen(
               self.get_correct_url(url), timeout=10
            )
        except urllib.error.HTTPError as ex:
            conn = ex
        except urllib.error.URLError:
            return 403
        return conn.getcode()

    @staticmethod
    @IgnoreInternetExceptions()
    def check_port(host: str, port: int):
        socket_connection = socket.socket()
        socket_connection.settimeout(10)
        try:
            socket_connection.connect((host, port))
        except (socket.gaierror, socket.timeout, ConnectionRefusedError, TimeoutError):
            return False
        return True

    @staticmethod
    @IgnoreInternetExceptions()
    def get_ip_from_host(host: str):
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            return False

    @IgnoreInternetExceptions()
    def __call__(self):
        # FIXME
        if self.data.host is not None:
            is_ip = re.findall(IP, self.data.host) != []
            if is_ip:
                ip = ".".join(re.findall(IP, self.data.host)[0])
                ip_status = self.get_ip_success(ip)
                if not isinstance(ip_status, InternetConnectionError) and not ip_status:
                    return CheckerException("ip is not success {0} {1}".format(ip, self.get_ip_success(ip)))
                if not self.check_port(ip, 443) or not self.check_port(ip, 80):
                    return CheckerException("HTTPS or HTT ports closed ({0})".format(ip))
                status_code = self.get_status_code(ip)
            else:
                if isinstance(self.get_ip_from_host(self.data.host), bool):
                    return CheckerException("can't get ip from the host ({0})".format(self.data.host))
                if self.data.host not in ["127.0.0.1", "localhost"]:
                    ip_status = self.get_ip_success(self.data.host)
                    if not ip_status and not isinstance(ip_status, InternetConnectionError):
                        return CheckerException("ip is not success ({0} {1})".format(
                            self.data.host, self.get_ip_success(self.data.host)
                        ))
                if self.data.ports is not None and self.data.host != "localhost":
                    if not self.check_port(self.data.host, 443) or not self.check_port(self.data.host, 80):
                        return CheckerException("HTTPS or HTT ports closed {0}".format(self.data.host))
                status_code = self.get_status_code(self.data.host)
            if status_code // 100 == 5:
                return CheckerException("server error ({0})".format(status_code))
            # if status_code // 100 == 4:
            #     return CheckerException("client error ({0})".format(status_code))

            host_display_name = "???" if is_ip else self.data.host
            host_ip = self.get_ip_from_host(self.data.host)
            host_ip = [host_ip] if isinstance(host_ip, str) else host_ip

            if isinstance(host_ip, InternetConnectionError):
                return host_ip

            if self.data.ports is None:
                return [host_display_name, host_ip, self.data.ports], \
                    "{0}\t|\t{1}\t|\t{2}\t|\t{3}\t|\t{4:.3} ms\t|\t-1\t|\t???".format(
                        datetime.now(), host_display_name, host_ip, 0.0,
                        ping(host_ip, timeout=500, unit="ms")
                    )
            elif self.data.host in ["127.0.0.1", "localhost"] and self.data.ports == []:
                return "{0}\t|\t{1}\t|\t{2}\t|\t0.0\t|\t{3:.3} ms\t|\t-1\t|\t???".format(
                    datetime.now(), host_display_name, host_ip[0],
                    ping(host_ip[0], timeout=500, unit="ms")
                )
            else:
                result = ""
                for ip in host_ip:
                    for port in self.data.ports:
                        result += "{0}\t|\t{1}\t|\t{2}\t|\t0.0\t|\t{3:.3} ms\t|\t{4}\t|\t{5}\n".format(
                            datetime.now(), host_display_name, ip,
                            ping(ip, timeout=500, unit="ms"), port,
                            "Opened" if self.check_port(ip, port) else "Not opened"
                        )
                if result[-1:] == "\n":
                    return result[:-1]
                return result

    def __repr__(self):
        return "Controller({0})".format(repr(self.data))
