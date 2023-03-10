import re
import socket
import requests
import urllib.error
import urllib.request

from ping3 import ping

from checker.units.exceptions import (
    IgnoreInternetExceptions, CheckerException, InternetConnectionError
)
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
            data = []
            for i in socket.getaddrinfo(host, 80):
                data.append(i[-1][0])
            return set(data)
        except socket.gaierror:
            return False

    @staticmethod
    @IgnoreInternetExceptions()
    def get_host_from_ip(host: str):
        try:
            return socket.gethostbyaddr(host)
        except socket.gaierror:
            return False

    @IgnoreInternetExceptions()
    def __call__(self):
        if self.data.host is not None:
            is_ip = re.findall(IP, self.data.host) != []
            if is_ip:
                ip = ".".join(re.findall(IP, self.data.host)[0])
                ip_status = self.get_ip_success(ip)
                if not isinstance(ip_status, InternetConnectionError) and not ip_status:
                    return CheckerException("ip is not success ({0})".format(ip, self.get_ip_success(ip)))
                if not self.get_host_from_ip(ip):
                    return CheckerException("cant get host name by address")
                if not self.check_port(ip, 443) or not self.check_port(ip, 80):
                    return CheckerException("HTTPS or HTT ports closed ({0})".format(ip))
                status_code = self.get_status_code(ip)
            else:
                if isinstance(self.get_ip_from_host(self.data.host), bool):
                    return CheckerException("can't get ip from the host ({0})".format(self.data.host))
                if self.data.host not in ["127.0.0.1", "localhost"]:
                    ip_status = self.get_ip_success(self.data.host)
                    if not ip_status and not isinstance(ip_status, InternetConnectionError):
                        return CheckerException("ip is not success ({0})".format(self.data.host))
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

            if isinstance(host_ip, InternetConnectionError):
                return host_ip

            host_ip = list(host_ip)

            if self.data.ports is None:
                return dict(
                    host_name=host_display_name,
                    host_ip=host_ip, ping=ping(host_ip, timeout=500, unit="ms")
                )
            elif self.data.host in ["127.0.0.1", "localhost"] and self.data.ports == []:
                return dict(
                    host_name="localhost",
                    host_ip="127.0.0.1", ping=ping(host_ip[0], timeout=500, unit="ms")
                )
            else:
                result = []
                for ip in host_ip:
                    for port in self.data.ports:
                        if len(re.findall(IP, ip)) != 0:
                            result.append(
                                dict(
                                    host_name=host_display_name, host_ip=ip,
                                    ping=ping(ip, timeout=500, unit="ms"), port=port,
                                    port_status="Opened" if self.check_port(ip, port) else "Not opened"
                                )
                            )
                return result

    def __repr__(self):
        return "Controller({0})".format(repr(self.data))
