"""
This module defines PI API Web client.
.. since: 0.2
"""

# -*- coding: utf-8 -*-
# Copyright (c) 2022 Endeavour Mining
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to read
# the Software only. Permissions are hereby NOT GRANTED to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# pylint: disable=W0221,C0116,E1101

import requests  # type: ignore
from requests import Response
from requests.models import PreparedRequest  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from requests.auth import HTTPBasicAuth  # type: ignore
from urllib3 import Retry  # type: ignore
from urllib3.exceptions import InsecureRequestWarning  # type: ignore


class TimeoutHTTPAdapter(HTTPAdapter):
    """
    A custom HTTP Adapter to handle session timeout for each request
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Ctor.
        :param args: Arguments
        :param kwargs: Other arguments
        """
        self.timeout = 3  # 3 seconds
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request: PreparedRequest, **kwargs) -> Response:
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class PiWebAPIClient:
    """
    PI Web API client.
    .. since: 0.2
    """

    def __init__(self, base_url, verify=None, **kwargs):
        """
        Ctor.
        :param base_url: Base url
        :param verify: Verify
        :param kwargs: Other arguments
        """
        self.base_url = base_url
        self.__adapter = TimeoutHTTPAdapter()
        if kwargs.get('session_timeout') is not None:
            self.__adapter = TimeoutHTTPAdapter(timeout=kwargs.get('session_timeout'))
        self.__adapter.max_retries = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["GET"]
        )
        self.__s = requests.Session()
        self.__s.mount("https://", adapter=self.__adapter)
        self.__s.mount("http://", adapter=self.__adapter)
        self.__s.headers.update({"accept": "application/json"})
        if verify is not None:
            self.__s.verify = verify
        else:
            self.__s.verify = False
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.__s.auth = HTTPBasicAuth(self.username, self.password)

    def get(self, endpoint: str = "", headers=None) -> Response:
        """
        Gets result.
        :param endpoint: Endpoint
        :param headers: Headers
        :return: Response
        """
        if headers is None:
            headers = {}
        return self.__s.get(
            url=self.base_url + endpoint,
            headers=headers
        )

    def delete(self, endpoint: str = "", headers=None) -> Response:
        if headers is None:
            headers = {}
        headers["x-requested-with"] = "piwebapiclient"
        return self.__s.delete(
            url=self.base_url + endpoint,
            headers=headers
        )

    def post(self, endpoint: str = "", headers=None, body: str = "") -> Response:
        """
        Post.
        :param endpoint: Endpoint
        :param headers: Headers
        :param body: Body
        :return: Response
        """
        if headers is None:
            headers = {}
        self.__add_headers(headers)
        return self.__s.post(
            url=self.base_url + endpoint,
            headers=headers,
            json=body
        )

    def put(self, endpoint: str = "", headers=None, body: str = "") -> Response:
        if headers is None:
            headers = {}
        self.__add_headers(headers)
        return self.__s.put(
            url=self.base_url + endpoint,
            headers=headers,
            json=body
        )

    def patch(self, endpoint: str = "", headers=None, body: str = "") -> Response:
        if headers is None:
            headers = {}
        self.__add_headers(headers)
        return self.__s.patch(
            url=self.base_url + endpoint,
            headers=headers,
            json=body
        )

    @staticmethod
    def __add_headers(headers) -> None:
        headers.update({"content-type": "application/json"})
        headers.update({"x-requested-with": "piwebapiclient"})
