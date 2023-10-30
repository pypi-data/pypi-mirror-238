#!/usr/bin/env python
#
# Copyright (c) 2022-2023 Subfork. All rights reserved.
#

__doc__ = """
Contains subfork task api classes and functions.
"""

import sys
import copy
import json

from subfork.api.base import Base
from subfork.logger import log


def is_valid_task(task_data):
    """Returns True if task is valid."""

    try:
        if not task_data:
            return False
        if "id" not in task_data:
            return False
        if "results" in task_data:
            task_data["results"] = sanitize_data(task_data["results"])
        json.dumps(task_data)
        assert sys.getsizeof(task_data) < 10240, "task data too large"

    except AssertionError as err:
        log.warning(err)
        return False

    except TypeError as err:
        log.warning("task data is not json serializable: %s" % err)
        return False

    return True


def sanitize_data(data, default=""):
    """
    Validates worker function results. Returns input data
    or an empty dict.

    :param data: data dict to sanitize
    :param default: default value if data is None
    """

    try:
        if data is None:
            data = default
        json.dumps(data)
        assert sys.getsizeof(data) < 8192, "data too large"

    except AssertionError as err:
        log.warning(err)
        return {}

    except TypeError as err:
        log.warning("task data is not json serializable: %s" % err)
        return {}

    return data


class Queue(Base):
    """Subfork Task Queue class."""

    def __init__(self, client, name):
        """ "
        :param client: Subfork client instance
        :param name: Queue name
        """
        super(Queue, self).__init__(client)
        self.name = name

    def __repr__(self):
        return "<Queue %s>" % self.name

    @classmethod
    def get(cls, client, name):
        return cls(client, name)

    def create_task(self, data=None):
        """
        Adds a task to a this Queue.

        :param data: kwarg dict passed to worker function
        :returns: Task instance
        """
        results = self.client._request(
            "task/create",
            data={
                "queue": self.name,
                "data": sanitize_data(data, default=None),
            },
        )
        if is_valid_task(results):
            return Task(self.client, self, results)
        return None

    def dequeue_task(self):
        """
        Dequeues next Task from this Queue.

        :returns: Task instance or None
        """
        results = self.client._request(
            "task/dequeue",
            data={
                "queue": self.name,
            },
        )
        if is_valid_task(results):
            return Task(self.client, self, results)
        return None

    def get_task(self, taskid):
        """
        Gets a task for a given queue name and task id.

        :param taskid: the id of the task to get
        :returns: Task instance or None
        """
        results = self.client._request(
            "task/get",
            data={
                "queue": self.name,
                "taskid": taskid,
            },
        )
        if is_valid_task(results):
            return Task(self.client, self, results)
        return None

    def length(self):
        """
        Returns the current size of a given queue.

        :returns: Number of Tasks in the Queue
        """
        resp = self.client._request(
            "queue/size",
            data={
                "queue": self.name,
            },
        )
        if type(resp) != int:
            log.debug("%s: bad response from server: %s" % (self.name, resp))
            return 0
        return resp


class Task(Base):
    """Subfork Task class."""

    def __init__(self, client, queue, data):
        """ "
        :param client: Subfork client instance
        :param queue: Queue instance
        :param data: Task data
        """
        super(Task, self).__init__(client, data)
        self.queue = queue

    def __repr__(self):
        return "<Task %s [%s]>" % (self.queue.name, self.data().get("id"))

    def get_num_failures(self):
        """Returns number of execution failures."""
        return self.data().get("failures", 0)

    def get_worker_data(self):
        """Returns worker function data."""
        return self.data().get("data", {})

    def is_valid(self):
        """Returns True if Task data is valid."""
        return is_valid_task(self.data())

    def requeue(self):
        """
        Requeues a task with a given task id.

        :returns: True if task was requeued
        """
        return self.client._request(
            "task/requeue",
            data={
                "queue": self.queue.name,
                "taskid": self.data().get("id"),
            },
        )

    def update(self, data, save=False):
        """
        Update and optionally save Task.

        :param data: Data dict to add to Task data
        :param save: Save this Task (optional)
        """
        self.data().update(data)
        if save:
            return self.save()
        return True

    def save(self):
        """Posts Task data to server."""
        if self.is_valid():
            task_data = copy.deepcopy(self.data())
            results = self.client._request(
                "task/save",
                data={
                    "queue": self.queue.name,
                    "taskid": self.data().get("id"),
                    "data": task_data,
                },
            )
            if is_valid_task(results):
                return Task(self.client, self, results)
        else:
            log.warning("invalid task data: %s" % self)
        return False


class Worker(Base):
    """Subfork Task Worker class."""

    def __init__(self, client, config):
        """ "
        :param client: Subfork client instance
        :param config: Worker config
        """
        super(Worker, self).__init__(client, config)

    def __repr__(self):
        return "<Worker %s>" % self.data().get("name")
