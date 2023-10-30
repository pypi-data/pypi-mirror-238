#!/usr/bin/env python
#
# Copyright (c) 2022-2023 Subfork. All rights reserved.
#

__doc__ = """
Contains subfork api config and settings.
"""

import os


def get_config(key, default=None):
    """Returns config setting from env, then config file."""

    return os.getenv(key, settings.get(key, default))


def get_config_file():
    """Returns path to config file. Order of priority:

        $SUBFORK_CONFIG_FILE
        $CWD/subfork.yaml

    :returns: config file path
    """

    config_file = os.path.join(os.getcwd(), "subfork.yaml")
    return os.getenv("SUBFORK_CONFIG_FILE", config_file)


def load_file(filename):
    """Reads a given config file and returns data dict.

    :param filename: config file path
    :returns: config data as a dict
    """

    data = {}

    if not os.path.exists(filename):
        return data

    import yaml

    with open(filename) as stream:
        try:
            data.update(yaml.safe_load(stream))
        except yaml.YAMLError as e:
            raise Exception("invalid config file: %s" % filename)
        except yaml.parser.ParserError as e:
            raise Exception("invalid config file: %s" % filename)

    return data


# get and load config file settings
config_file = get_config_file()
settings = load_file(config_file)

# global debug switch
DEBUG = get_config("DEBUG", False) in (1, "1", True, "True")

# remote host settings
HOST = get_config("SUBFORK_HOST")
PORT = get_config("SUBFORK_PORT", 80)

# which api version endpoint to use
API_VERSION = get_config("SUBFORK_API_VERSION", "api")

# get access keys
ACCESS_KEY = get_config("SUBFORK_ACCESS_KEY")
SECRET_KEY = get_config("SUBFORK_SECRET_KEY")

# auto minimize js and css files
AUTO_MINIMIZE = get_config("AUTO_MINIMIZE", False)

# subfork site template file
TEMPLATE_FILE = get_config("TEMPLATE_FILE", "template.yaml")

# automatically restart workers when config file changes
AUTO_RESTART_WORKERS = get_config("AUTO_RESTART", True)

# worker settings (contains namespaced worker settings)
WORKER = get_config("WORKER", {})

# maximum number of tasks to process at once
TASK_BATCH_SIZE = int(get_config("SUBFORK_TASK_BATCH_SIZE", 100))

# default worker function
TASK_FUNCTION = get_config("SUBFORK_TASK_FUNC", "subfork.worker.test")

# name of the default task queue
TASK_QUEUE = get_config("SUBFORK_TASK_QUEUE", "test")

# task dequeue rate throttle (dequeue wait time in seconds)
TASK_RATE_THROTTLE = float(get_config("TASK_RATE_THROTTLE", 0.1))

# maximum number of task retry attempts
TASK_MAX_RETRY_LIMIT = 3

# default failure retry limit
TASK_RETRY_LIMIT = int(get_config("TASK_RETRY_LIMIT", 2))

# minimum wait time between queue checks
MIN_WAIT_TIME = 30

# default request interval in seconds
WAIT_TIME = float(get_config("REQUEST_INTERVAL", MIN_WAIT_TIME))

# ignorable file patterns when deploying
IGNORABLE = [
    "*~",
    "*.bat",
    "*.bak",
    "*.dll",
    "*.exe",
    ".git*",
    "*.jar",
    "*.php",
    "*.py",
    "*.pyc",
    "*.reg",
    "*.sh",
    "*.slo",
    "*.so",
    "*.tmp",
    "venv*",
    "*.zip",
    "__pycache__",
    "Thumbs.db",
    ".DS_Store",
]
