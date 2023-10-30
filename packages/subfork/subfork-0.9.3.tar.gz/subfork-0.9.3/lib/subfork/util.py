#!/usr/bin/env python
#
# Copyright (c) 2022-2023 Subfork. All rights reserved.
#

__doc__ = """
Contains utility functions and classes.
"""

import os
import re
import sys
import time
import yaml
import requests
import fnmatch
from functools import wraps

import subfork
from subfork import config
from subfork.logger import log
from subfork.version import __prog__, __version__

# store current working directory
CWD = os.getcwd()

# make a regex that matches ignorable file patterns
IGNORABLE_PATHS = re.compile(
    "(" + ")|(".join([fnmatch.translate(i) for i in config.IGNORABLE]) + ")"
)

# define some times
HOURS_1 = 3600
HOURS_6 = 21600
HOURS_12 = 43200
HOURS_24 = 86400


def b2h(bytes, format="%(value).1f%(symbol)s"):
    """Converts bytes to a human readable format."""
    symbols = ("B", "K", "M", "G", "T")
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(symbols[1:]):
        if bytes >= prefix[symbol]:
            value = float(bytes) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=bytes)


def check_version():
    """Checks PyPI for version updates."""

    try:
        name = "%s %s" % (__prog__, __version__)

        pypi_url = "https://pypi.org/pypi/%s/json" % __prog__
        request = requests.get(pypi_url)

        if request.status_code == 404:
            log.warning("package %s not found in PyPI", __prog__)

        elif request.status_code == 200:
            all_versions = sorted(list(request.json()["releases"].keys()))
            latest_version = all_versions[-1]
            if __version__ not in all_versions:
                log.warning("%s not found in PyPI" % name)
                return False
            elif __version__ != latest_version:
                log.warning("newer version available: %s", latest_version)
                return False

        else:
            log.debug("PyPI returned code %s", request.status_code)

        return True

    except Exception as e:
        log.error("error getting version: %s", str(e))

    return


def checksum(filepath):
    """Returns an MD5 checksum for a given filepath."""

    import io
    import hashlib

    with open(filepath, "rb") as file:
        md5_hash = hashlib.md5()
        while True:
            data = file.read(io.DEFAULT_BUFFER_SIZE)
            if not data:
                break
            md5_hash.update(data)

    return md5_hash.hexdigest()


def create_zip_file(targets, outfile=None):
    """Creates a zip file for a given list of target dirs."""
    import zipfile

    def zipdir(path, ziph):
        os.chdir(path)
        for root, _, files in os.walk("."):
            for f in files:
                ziph.write(os.path.join(root, f))

    if not outfile:
        outfile = "subfork.zip"

    zipf = zipfile.ZipFile(outfile, "w", zipfile.ZIP_DEFLATED)
    for target in targets:
        if os.path.exists(target):
            zipdir(target, zipf)
    zipf.close()

    return outfile


def deprecated(f):
    """Decorator that logs deprecation warning."""

    @wraps(f)
    def decorated(*args, **kwargs):
        log.warning("%s is deprecated", f.__name__)
        return f(*args, **kwargs)

    return decorated


def encodeurl(params):
    """python 2/3 compatible url encoder."""

    try:
        from urllib.parse import urlencode
    except Exception:
        from urllib import urlencode

    return urlencode(params)


def get_client(host=config.HOST, port=config.PORT):
    """Returns a client connection object."""

    try:
        return subfork.Subfork(
            host=host,
            port=port,
            access_key=config.ACCESS_KEY,
            secret_key=config.SECRET_KEY,
        )

    except (subfork.client.RequestError, subfork.client.ConnectError):
        log.error("could not connect to %s", host)
        raise


def get_mime_type(filename):
    """Returns the MIME type for a given filename."""

    import mimetypes

    mime_types = {
        ".bmp": "image/bmp",
        ".css3": "text/css",
        ".gz": "application/gzip",
        ".map": "application/json",
    }

    mime_type, _ = mimetypes.guess_type(filename)
    _, ext = os.path.splitext(filename)
    mime_type = mime_types.get(ext, mime_type)

    if mime_type:
        return mime_type
    else:
        return "octet/binary-stream"


def get_python_version():
    """Returns Python version as major.minor."""
    return ".".join(map(str, sys.version_info[0:2]))


def get_session_id():
    """Returns unique session id."""
    import uuid

    return str(uuid.uuid4())


def get_status_message(status_code):
    """Returns a status code message."""
    return {
        400: "bad request",
        401: "unauthorized",
        402: "payment required",
        403: "forbidden",
        404: "not found",
        405: "method not allowed",
        408: "request timed out",
        413: "payload too large",
        417: "missing parameters",
        423: "locked",
        426: "update required",
        429: "too many requests",
        500: "there was a server error",
        504: "gateway timeout",
    }.get(status_code, "unhandled error: %s" % status_code)


def get_time():
    """Returns epoch time in millis as an int."""
    return int(time.time() * 1000.0)


def get_version():
    """Returns subfork version as a string."""
    from subfork.version import __version__
    return __version__


def is_ignorable(path):
    """Returns True if path is ignorable."""
    if path.startswith("."):
        return True
    return re.search(IGNORABLE_PATHS, path) is not None


def is_subpath(filepath, directory):
    """Returns True if the common prefix of both is equal."""
    d = os.path.join(os.path.realpath(directory), "")
    f = os.path.realpath(filepath)
    return os.path.commonprefix([f, d]) == d


def minify(src, dst):
    """Minify a given src file and output to a dst file."""
    minimized_src = minify_file(src)
    if minimized_src:
        fp = open(dst, "w")
        fp.write(minimized_src)
        fp.close()
    else:
        print("error minify'ing source")


def minify_file(filepath):
    """Returns minified file contents."""
    minified = ""

    if not os.path.exists(filepath):
        log.warning("file not found: %s" % filepath)

    else:
        try:
            from jsmin import jsmin

            with open(filepath) as js_file:
                minified = jsmin(js_file.read(), quote_chars="'\"`")

        except Exception as e:
            log.error(e)

    return minified


def normalize_path(path, start=os.getcwd()):
    """Returns a normalized path."""

    npath = os.path.normpath(path)

    if start is None or is_subpath(path, start):
        return os.path.relpath(npath, start=start).replace("\\", "/")

    return os.path.abspath(npath).replace("\\", "/")


def read_zip_file(filepath):
    """File reader data generator."""

    # work in chunks to limit mem usage when reading
    BUF_SIZE = 65536

    binary_content = b""
    start = time.time()

    # time limit in secs
    limit = 10

    def read_file_gen():
        with open(filepath, "rb") as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                if (time.time() - start) > limit:
                    break
                yield data

    for data in read_file_gen():
        binary_content += data

    return binary_content


def read_template(template_file):
    """Reads a template.yaml file and returns template data as a dict.

    :param template_file: input template.yaml file
    :returns: template data dict
    """

    if not os.path.exists(template_file):
        return

    with open(template_file) as stream:
        data = yaml.safe_load(stream)

    return data


def write_template(template_file, template_data):
    """Writes template data to filepath.

    :param template_file: template.yaml file path
    :param template_data: template data dict
    """

    fp = open(template_file, "w")
    fp.write(yaml.dump(template_data))
    fp.close()

    return template_file


def splitext(src):
    """Returns tuple of relative file path and file extension.

    :param src: source file path
    :returns: (rel file path, file extension)
    """

    try:
        name = src.split(CWD)[-1]

    except Exception:
        name = os.path.basename(src)

    _, ext = os.path.splitext(name)
    return name, ext


def walk(path):
    """Generator that yields found filepaths."""

    if not is_ignorable(path) and os.path.isfile(path):
        yield path

    path = os.path.abspath(path)
    for dirname, dirs, files in os.walk(path, topdown=True):
        if is_ignorable(dirname):
            continue
        for d in dirs:
            if is_ignorable(d):
                dirs.remove(d)
        for name in files:
            if not is_ignorable(name):
                yield os.path.join(dirname, name)


def write_file(filepath, content):
    """Writes text content to a filepath."""

    dirname = os.path.dirname(filepath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    fp = open(filepath, "w")
    fp.write(content)
    fp.close()
