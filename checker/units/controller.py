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
import re
import socket
import requests
import urllib.error
import urllib.request

from ping3 import ping
from typing import Union, Any

from checker.units.exceptions import (
    IgnoreInternetExceptions, CheckerException, InternetConnectionError, SSCException
)
from checker.units.reader import ReadObject
from checker.config import IP
from checker.config import headers

__all__ = ("Controller", )

class Controller(object):
    r"""
    A class that conducts all the necessary checks for a single site

    get_correct_url(url: str) -> str
        The function for getting the correct type of link (http://url/)
    get_ip_success(ip: str) -> bool
        The function that checks the availability of the ip address of the site
    get_status_code(url: str) -> int
        The function that returns a code after a get request to the site
    check_port(host: str, port: int) -> bool
        The function checking port availability (closed or open)
    get_ip_from_host(host: str) -> Union[set, bool]
        The function that gets an IP address from a domain name
    get_host_from_ip(host: str) -> Union[bool, socket.gethostbyaddr]
        The function that gets a domain name by IP address
    check_domains(self, host: str, ports: Union[int, list]) -> Any
        The function that conducts all basic checks for the site
    __call__(self) -> Any
        The method performs all necessary checks for the site and returns
    """
    __slots__ = (
        "target",
    )
    def __init__(self, target: ReadObject) -> None:
        self.target: ReadObject = target

    @staticmethod
    @IgnoreInternetExceptions()
    def get_correct_url(url: str) -> str:
        r"""
        The function for getting the correct type of link (http://url/)

        Parameters
        ------------
            url: str
                Link to format

        Returns
        --------
            Formatted link (str)
        """
        if "http://" in url or "https://" in url:
            return url
        return "http://" + url

    @IgnoreInternetExceptions(check_ip=True)
    def get_ip_success(self, ip: str) -> bool:
        r"""
        The function that checks the availability of the ip address of the site

        Parameters
        ------------
            ip: str
                IP address to check

        Returns
        --------
            Returns the availability status of an ip address (str)
        """
        try:
            requests.get(
                self.get_correct_url(ip), timeout=5,
                headers=headers
            )
        except requests.exceptions.Timeout:
            return False
        return True

    @IgnoreInternetExceptions()
    def get_status_code(self, url: str) -> int:
        r"""
        The function that returns a code after a get request to the site

        Parameters
        ------------
            url: str
                Link to get response status code

        Returns
        --------
            Response status code (int)
        """
        try:
            conn = urllib.request.urlopen(
               self.get_correct_url(url), timeout=5
            )
        except urllib.error.HTTPError as ex:
            conn = ex
        except urllib.error.URLError:
            return 403
        return conn.getcode()

    @staticmethod
    @IgnoreInternetExceptions()
    def check_port(host: str, port: int) -> bool:
        r"""
        The function checking port availability (closed or open)

        Parameters
        ------------
            host: str
                Domain name needed to check the port
            port: str
                port to check (closed or open)

        Returns
        ------------
            Port availability (closed or open) (bool)
        """
        socket_connection = socket.socket()
        socket_connection.settimeout(5)
        try:
            socket_connection.connect((host, port))
        except (socket.gaierror, socket.timeout, ConnectionRefusedError, TimeoutError):
            return False
        return True

    @staticmethod
    @IgnoreInternetExceptions()
    def get_ip_from_host(host: str) -> Union[set, bool]:
        r"""
        The function that gets an IP address from a domain name

        Parameters
        ------------
            host: str
                Domain name to be expanded into one or more IP addresses

        Returns
        ------------
            One or more IP addresses or False
            (if it was not possible to get the IP address)
            (Union[set, bool])
        """
        try:
            data = []
            for i in socket.getaddrinfo(host, 80):
                data.append(i[-1][0])
            return set(data)
        except socket.gaierror:
            return False

    @IgnoreInternetExceptions()
    def get_host_from_ip(self, host: str) -> Union[bool, socket.gethostbyaddr]:
        r"""
        The function that gets a domain name by IP address

        Parameters
        ------------
            host: str
                IP address to be expanded into a domain name

        Returns
        ------------
            Returns the domain name if possible, false otherwise (Union[bool, socket.gethostbyaddr])
        """
        try:
            return socket.gethostbyaddr(host)
        except (socket.gaierror, socket.herror):
            return False

    def check_domains(self, host: str, ports: Union[int, list]) -> Any:
        r"""
        The function that conducts all basic checks for the site

        Parameters
        ------------
            host: str
                Domain name or IP address for which you want to
                perform all the necessary checks for errors
            ports: Union[int, list]
                Port or ports to check for errors

        Returns
        ------------
            Error class with message or status IP or domain name (Any)
        """
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
    def __call__(self) -> Any:
        r"""
        The method performs all necessary checks for the site and returns

        Returns
        ------------
            The method returns the result of the check for one site (Any)
        """
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
            host_ping = ping(host_ip[0], timeout=5, unit="ms")
            return dict(
                host_name="localhost",
                host_ip="127.0.0.1",
                ping=5000 if host_ping is None else host_ping,
                status=len(host_ip) > 1
            )

        if not self.target.ports:
            result = []

            for ip in host_ip:
                host_ping = ping(ip, timeout=5, unit="ms")
                result.append(
                    dict(
                        host_name=host_display_name,
                        host_ip=ip,
                        ping=5000 if host_ping is None else host_ping,
                        status=len(host_ip) > 1
                    )
                )
            return result
        else:
            result = []

            for ip in host_ip:
                for port in self.target.ports:
                    host_ping = ping(ip, timeout=5, unit="ms")
                    result.append(
                        dict(
                            host_name=host_display_name,
                            host_ip=ip,
                            ping=5000 if host_ping is None else host_ping,
                            port=port,
                            port_status="Opened" if self.check_port(ip, port) else "Not opened",
                            status=len(host_ip) > 1
                        )
                    )
            return result

    def __repr__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, repr(self.target))
