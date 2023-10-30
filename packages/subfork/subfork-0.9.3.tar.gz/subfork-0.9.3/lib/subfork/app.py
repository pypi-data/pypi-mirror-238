#!/usr/bin/env python
#
# Copyright (c) 2022-2023 Subfork. All rights reserved.
#

__doc__ = """
Contains subfork dev server classes and functions.
"""

import os
import sys
import signal
import time
import webbrowser
from functools import wraps

import flask

import subfork
from subfork import config
from subfork import util
from subfork.worker import StoppableThread
from subfork.logger import log, setup_stream_handler

setup_stream_handler("subfork")

# global list of templates
templates = []


def client_required(f, client):
    """Decorator that passes client to wrapped function."""

    @wraps(f)
    def decorated(*args, **kwargs):
        return f(client, **kwargs)

    return decorated


def catch_all(client, path):
    """Catch-all page request handler."""
    return "requested path: %s" % path


def api_request(client, **kwargs):
    """API endpoint stub handler."""

    data = flask.request.get_json()
    error = None
    results = {}
    success = False
    url = "/".join(list(kwargs.values()))

    try:
        results = client._request(url, data)
        success = True

    except Exception as e:
        log.error(e)
        error = str(e)

    finally:
        return flask.jsonify(
            {
                "error": error,
                "data": results,
                "success": success,
                "total_count": len(results),
            }
        )


def read_page_configs(template_data):
    """
    Reads subfork config file and returns route->page map.

    :param template_data: config file data.
    """

    route_map = {}

    for _, page_config in template_data.get("pages", {}).items():
        route_map.update(
            {
                page_config.get("route"): {
                    "attrs": page_config.get("attrs", {}),
                    "file": page_config.get("file"),
                }
            }
        )

    return route_map


class MockUser(object):
    """Mock user class for testing."""

    def __init__(self, client, data):
        self.client = client
        self.data = data
        self.is_authenticated = True

    def __getattr__(self, key):
        return self.data.get(key)


def render_wrapper(client, template_folder, template, page_config):
    """Decorator that wraps the render template function.

    :param client: Subfork client instance
    :param template_folder: templates folder
    :param template: template file name
    :param page_config: page config
    """

    def render(**kwargs):
        log.debug("render: %s", template)

        login_required = page_config.get("login_required")
        page_attrs = page_config.get("attrs")
        _, ext = os.path.splitext(template)

        # jinja stubs
        kwargs.update(
            {
                "args": flask.request.args,
                "get_user": client.get_user,
                "page": {
                    "attrs": page_attrs,
                    "site": client.site().data(),
                },
                "site": client.site().data(),
                "user": MockUser(client, client.user().data()),
            }
        )

        try:
            if ext in (
                ".html",
                ".htm",
            ):
                return flask.render_template(template, **kwargs)
            source = open(os.path.join(template_folder, template), "r").read()
            mimetype = util.get_mime_type(template)
            return flask.Response(source, mimetype=mimetype)

        except subfork.client.RequestError as e:
            log.error("response from server: %s", str(e))
            return str(e)

        except Exception as e:
            log.exception(e)
            return flask.abort(500)

    render.__name__ = "render_%s" % len(templates)
    templates.append(render)

    return render


class App(flask.Flask):
    """Development server app class."""

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.setup_logger()

    def setup_logger(self):
        """Redirects werkzeug logger."""
        import logging
        from werkzeug.serving import WSGIRequestHandler

        werkzeug_logger = logging.getLogger("werkzeug")
        WSGIRequestHandler.log.debug = log.debug
        WSGIRequestHandler.log.info = log.info


class DevServer(StoppableThread):
    """Thread that runs an instance of the dev server app."""

    def __init__(self, host, port, config_file):
        super(DevServer, self).__init__()
        self.config_file = config_file
        self.host = host
        self.port = port

    def run(self):
        """Called when the thread starts."""
        app = create_app(self.config_file)
        return run_app(app, self.host, self.port)


def create_app(config_file):
    """
    Creates and returns an instance of the dev server for testing.

    :param config_file: file path to subfork template file.
    """

    # read subfork site template file
    root_folder = os.path.dirname(config_file)
    template_data = util.read_template(config_file)

    # get template and static file folders
    template_folder = os.path.join(
        root_folder, template_data.get("template_folder", "templates")
    )
    static_folder = os.path.join(
        root_folder, template_data.get("static_folder", "static")
    )

    # create the client
    client = util.get_client(config.HOST, config.PORT)

    # create an app instance and set template and static folders
    log.debug("template_folder: %s", template_folder)
    log.debug("static_folder: %s", static_folder)
    app = App(
        client.site().data().get("name"),
        template_folder=template_folder,
        static_folder=static_folder,
    )
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # api endpoint stub
    app.route("/api/<obj>/<op>", methods=["POST"])(client_required(api_request, client))

    # catch-all page endpoint stub
    app.route("/<path:path>", methods=["GET"])(client_required(catch_all, client))

    # get the routes and pages from the config data
    page_configs = read_page_configs(template_data)

    # configure dev page routes
    for route, page_config in sorted(page_configs.items(), key=lambda x: len(x[0])):
        try:
            template_file = page_config.get("file")
            log.debug("route %s -> template %s", route, template_file)
            app.route(route, methods=["GET"])(
                render_wrapper(client, template_folder, template_file, page_config)
            )

        except Exception:
            log.exception("error creating route: %s", route)

    return app


def run_app(app, host="localhost", port=8080):
    """
    Run the dev server for testing.

    :param app: dev server app instance.
    :param host: dev server host (default localhost).
    :param port: dev server port (default 8080).
    """

    return app.run(host=host, debug=False, port=port, threaded=False)


def start_running():
    """Sets global running variable to True."""
    global running
    running = True


def is_running():
    """Returns value of global running variable."""
    global running
    return running


def run(host, port, config_file):
    """
    Starts a simple dev server process, and opens a webbrowser to
    the running dev server.

    :param host: dev server host.
    :param port: dev server port.
    :param config_file: file path to subfork site template.
    """

    def pause():
        if sys.platform == "win32":
            while is_running():
                time.sleep(1)
        else:
            signal.pause()

    if not os.path.exists(config_file):
        log.error("config file not found: %s", config_file)
        return 2

    try:
        # start up the dev server in a thread
        log.info("template: %s", config_file)
        server = DevServer(host, port, config_file)
        server.start()

        # open the site
        log.info("dev server running at %s:%s", server.host, server.port)
        webbrowser.open("http://%s:%s" % (server.host, server.port))
        start_running()

        # wait for sigint
        pause()

    except KeyboardInterrupt:
        log.info("shutting down dev server")

    except Exception as e:
        log.exception("unexpected error: %s", str(e))
        return 1

    return 0
