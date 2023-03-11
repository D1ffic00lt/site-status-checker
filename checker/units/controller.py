# -*- coding:utf-8 -*-
import re
import socket
import requests
import urllib.error
import urllib.request

from ping3 import ping
from typing import Union

from checker.units.exceptions import (
    IgnoreInternetExceptions, CheckerException, InternetConnectionError, SSCException
)
from checker.units.reader import ReadObject
from checker.units.config import IP
from checker.units.config import headers

__all__ = ("Controller", )

class Controller(object):
    __slots__ = (
        "target",
    )
    def __init__(self, target: ReadObject) -> None:
        self.target: ReadObject = target

    @staticmethod
    @IgnoreInternetExceptions()
    def get_correct_url(url: str) -> str:
        if "http://" in url or "https://" in url:
            return url
        return "http://" + url

    @IgnoreInternetExceptions(check_ip=True)
    def get_ip_success(self, ip: str) -> str:
        try:
            requests.get(
                self.get_correct_url(ip), timeout=10,
                headers=headers
            )
        except requests.exceptions.Timeout:
            return False
        return True

    @IgnoreInternetExceptions()
    def get_status_code(self, url: str) -> int:
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
    def check_port(host: str, port: int) -> bool:
        socket_connection = socket.socket()
        socket_connection.settimeout(10)
        try:
            socket_connection.connect((host, port))
        except (socket.gaierror, socket.timeout, ConnectionRefusedError, TimeoutError):
            return False
        return True

    @staticmethod
    @IgnoreInternetExceptions()
    def get_ip_from_host(host: str) -> Union[set, bool]:
        try:
            data = []
            for i in socket.getaddrinfo(host, 80):
                data.append(i[-1][0])
            return set(data)
        except socket.gaierror:
            return False

    @staticmethod
    @IgnoreInternetExceptions()
    def get_host_from_ip(host: str) -> Union[bool, socket.gethostbyaddr]:
        try:
            return socket.gethostbyaddr(host)
        except socket.gaierror:
            return False

    def check_domains(self, host, ports):
        is_ip = re.findall(IP, host) != []

        if is_ip and "127.0.0.1" not in host:
            ip = ".".join(re.findall(IP, host)[0])
            ip_status = self.get_ip_success(ip)

            if not isinstance(ip_status, InternetConnectionError) and not ip_status:
                return CheckerException("ip is not success ({0})".format(ip, self.get_ip_success(ip)))

            if not self.get_host_from_ip(ip):
                return CheckerException("cant get host name by address")

            if not self.check_port(ip, 443) or not self.check_port(ip, 80):
                return CheckerException("HTTPS or HTT ports closed ({0})".format(ip))

            status_code = self.get_status_code(ip)
        else:
            if isinstance(self.get_ip_from_host(host), bool):
                return CheckerException("can't get ip from the host ({0})".format(host))

            if host not in ["127.0.0.1", "localhost"]:
                ip_status = self.get_ip_success(host)

                if not ip_status and not isinstance(ip_status, InternetConnectionError):
                    return CheckerException("ip is not success ({0})".format(host))

            if ports is not None and host not in ["localhost", "127.0.0.1"]:
                if not self.check_port(host, 443) or not self.check_port(host, 80):
                    return CheckerException("HTTPS or HTT ports closed {0}".format(host))

            status_code = self.get_status_code(host)
        if status_code // 100 == 5:
            return CheckerException("server error ({0})".format(status_code))
        return is_ip

    @IgnoreInternetExceptions()
    def __call__(self) -> Union[
        InternetConnectionError, CheckerException,
        set, dict[str, Union[str, float]], list[dict], str
    ]:
        if self.target.host is None:
            return
        is_ip = self.check_domains(self.target.host, self.target.ports)

        if isinstance(is_ip, SSCException):
            return is_ip

        host_display_name = "???" if is_ip else self.target.host
        host_ip = self.get_ip_from_host(self.target.host) if not is_ip else [self.target.host]

        if isinstance(host_ip, InternetConnectionError):
            return host_ip

        host_ip = list(filter(lambda x: len(re.findall(IP, x)) == 1, host_ip))

        if self.target.host in ["127.0.0.1", "localhost"]:
            return dict(
                host_name="localhost",
                host_ip="127.0.0.1",
                ping=ping(host_ip[0], timeout=500, unit="ms"),
                status=len(host_ip) > 1
            )

        if not self.target.ports:
            result = []

            for ip in host_ip:
                result.append(
                    dict(
                        host_name=host_display_name,
                        host_ip=ip,
                        ping=ping(ip, timeout=500, unit="ms"),
                        status=len(host_ip) > 1
                    )
                )
            return result
        else:
            result = []

            for ip in host_ip:
                for port in self.target.ports:
                    result.append(
                        dict(
                            host_name=host_display_name,
                            host_ip=ip,
                            ping=ping(ip, timeout=500, unit="ms"), port=port,
                            port_status="Opened" if self.check_port(ip, port) else "Not opened",
                            status=len(host_ip) > 1
                        )
                    )
            return result

    def __repr__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, repr(self.target))
