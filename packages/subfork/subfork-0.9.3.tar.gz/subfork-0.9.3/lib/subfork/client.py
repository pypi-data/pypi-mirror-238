#!/usr/bin/env python
#
# Copyright (c) 2022-2023 Subfork. All rights reserved.
#

__doc__ = """
Contains subfork client classes and functions.
"""

import sys
import json
import hashlib
import requests

import subfork.config as config
import subfork.util as util
from subfork.api.site import Site
from subfork.api.user import User
from subfork.logger import log, setup_stream_handler
from subfork.version import __prog__, __version__

setup_stream_handler(__prog__)


class ClientError(Exception):
    """Custom exception class for authentication errors."""

    pass


class ConfigError(Exception):
    """Custom exception class for config errors."""

    pass


class ConnectError(Exception):
    """Custom exception class for connection errors."""

    pass


class RequestError(Exception):
    """Custom exception class for request errors."""

    pass


class SubforkHttpClient(object):
    """General purpose HTTP Client for interacting with
    the Subfork REST API."""

    last_error = None
    last_request_ts = 0
    session = {}
    sessionid = None

    def __init__(
        self,
        host=config.HOST,
        port=config.PORT,
        api_version=config.API_VERSION,
        access_key=config.ACCESS_KEY,
        secret_key=config.SECRET_KEY,
    ):
        """
        Instantiates an instance of the Subfork Http client.

        :param host: site domain ($SUBFORK_HOST)
        :param port: site port ($SUBFORK_PORT)
        :param api_version: api endpoint to use ($SUBFORK_API_VERSION)
        :param access_key: access key ($SUBFORK_ACCESS_KEY)
        :param secret_key: secret key ($SUBFORK_SECRET_KEY)
        """
        super(SubforkHttpClient, self).__init__()
        self.host = host
        self.port = port
        self.base_url = "http://%s:%s" % (self.host, self.port)
        self.api_url = self.base_url + "/" + api_version
        self.auth = (access_key, secret_key)
        self.headers = {
            "sid": None,
            "user-agent": f"python-{__prog__}/{__version__}",
        }
        self.check_config()
        self.get_session_data()

    def __repr__(self):
        return "<SubforkHttpClient %s>" % self.host

    def __get_auth(self):
        return self.__auth

    def __set_auth(self, auth):
        access_key, secret_key = auth
        self.__auth = (
            access_key,
            hashlib.sha256(
                "{accesskey}:{secretkey}".format(
                    accesskey=access_key, secretkey=secret_key
                ).encode("utf-8")
            ).hexdigest(),
        )

    auth = property(__get_auth, __set_auth)

    def check_config(self):
        """Validates client connection configuration."""
        if not self.host:
            raise ConfigError("missing host")
        if not self.port:
            raise ConfigError("missing port")
        if not self.__auth:
            raise ConfigError("missing auth")

    def _request(self, url, data={}, file_data=None):
        """
        Makes an HTTP POST Request with data provided.

        :param url: API endpoint url
        :param data: request data (must be JSON serializable)
        :param file_data:
        :returns: response data
        """

        if file_data:
            if not url.endswith("deploy"):
                raise RequestError("invalid request")
            elif sys.getsizeof(file_data) > 2e6:
                raise RequestError("invalid request: file data too large")

        if (sys.getsizeof(data) > 10240) or len(data) > 25:
            log.error("invalid request: data too large")
            return {}

        self.last_request_ts = util.get_time()
        url = self.format_url(url)

        try:
            if file_data:
                resp = requests.post(
                    url,
                    auth=self.auth,
                    data=data,
                    headers=self.headers,
                    files={
                        "json": (None, json.dumps(data)),
                        "file": ("template.zip", file_data),
                    },
                )
            else:
                resp = requests.post(
                    url,
                    auth=self.auth,
                    headers=self.headers,
                    json=data,
                )
            return self.handle_response(resp)
        except RequestError as e:
            # self.last_error = str(e)
            log.warning("request error: %s" % e)
        except requests.exceptions.ConnectionError as e:
            self.last_error = str(e)
            log.warning("could not connect to host: %s" % self.host)
        return

    def format_url(self, url):
        """Returns a formatted api request url."""
        return "/".join([self.api_url, url])

    def handle_response(self, resp):
        """Request response handler."""
        if resp is None:
            log.warning("no response from server")
        elif resp.ok:
            if self.last_error:
                log.info("connection restored")
                self.last_error = None
            data = resp.json()
            error = data.get("error")
            success = data.get("success")
            if not success and error:
                log.warning(error)
            return data.get("data", None)
        else:
            status_message = util.get_status_message(resp.status_code)
            if resp.status_code == 500:
                log.warning(status_message)
            elif resp.status_code in (401, 402, 403):
                raise ClientError(status_message)
            else:
                raise RequestError(status_message)
        return None

    def get_session_data(self):
        """Requests and returns session data from remote server."""
        if self.session:
            return self.session
        self.session = self._request(
            "get_session_data",
            data={
                "source": "python-client",
                "version": util.get_version(),
            },
        )
        if self.session and self.session.get("sessionid"):
            self.sessionid = str(self.session["sessionid"])
        self.headers["sid"] = self.sessionid
        return self.session

    def get_session_token(self):
        """Return the session id for with the current connection."""
        if self.sessionid:
            return self.sessionid
        if self.session:
            self.sessionid = str(self.session.get("sessionid"))
        return self.sessionid


class Subfork(object):
    """
    Subfork API client class.

    Usage:

        # instantiate client
        >>> import subfork
        >>> sf = subfork.get_client()

        # get page
        >>> page = sf.get_page("test.html")

        # find data
        >>> dt = sf.get_data("test")
        >>> params = [["foo", "=", "bar"]]
        >>> records = dt.find(params)
    """

    __conn = None
    __site = None
    __user = None

    def __init__(
        self,
        host=config.HOST,
        port=config.PORT,
        api_version=config.API_VERSION,
        access_key=config.ACCESS_KEY,
        secret_key=config.SECRET_KEY,
    ):
        """
        Instantiates an instance of the Subfork API client.

        :param host: site domain ($SUBFORK_HOST)
        :param port: site port ($SUBFORK_PORT)
        :param api_version: api endpoint to use ($SUBFORK_API_VERSION)
        :param access_key: access key ($SUBFORK_ACCESS_KEY)
        :param secret_key: secret key ($SUBFORK_SECRET_KEY)
        """
        super(Subfork, self).__init__()
        Subfork._set_conn(host, port, api_version, access_key, secret_key)

    def __repr__(self):
        return "<Subfork %s>" % self.conn().host

    @classmethod
    def conn(cls):
        """Returns shared SubforkHttpClient object."""
        return cls.__conn

    @classmethod
    def _set_conn(cls, host, port, api_version, access_key, secret_key):
        """Establishes a shared server connection."""
        if not cls.__conn or cls.__conn.host != host:
            log.info("connecting to %s" % host)
            cls.__conn = SubforkHttpClient(
                host, port, api_version, access_key, secret_key
            )

    def _request(self, url, data={}, file_data=None):
        """Makes an Http request to the server and returns response data."""
        return self.conn()._request(url, data, file_data)

    def get_data(self, name):
        """
        Returns a Datatype object.

        :param name: datatype name, e.g. "test"
        :returns: data.Datatype instance
        """
        return self.site().get_data(name)

    def get_page(self, name):
        """
        Returns a Page object matching `name`.

        :param name: page name, e.g. "test.html"
        :returns: page.Page instance
        """
        return self.site().get_page(name)

    def get_queue(self, name):
        """
        Returns a Task Queue object.

        :param name: queue name, e.g. "test"
        :returns: task.Queue instance
        """
        return self.site().get_queue(name)

    def get_user(self, username):
        """
        Returns a subfork site user matching a given username.

        :param username: site username value
        :returns: user.User instance
        """
        return self.site().get_user(username)

    def site(self):
        """Returns shared Site object."""
        if not self.__site:
            self.__site = Site.get(self)
        return self.__site

    def user(self):
        """Returns API User object."""
        if not self.__user:
            self.__user = User(self, self.conn().session.get("user"))
        return self.__user
