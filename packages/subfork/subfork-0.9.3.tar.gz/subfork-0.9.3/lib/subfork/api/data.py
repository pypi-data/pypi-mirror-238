#!/usr/bin/env python
#
# Copyright (c) 2022-2023 Subfork. All rights reserved.
#

__doc__ = """
Contains subfork data api classes and functions.
"""

import sys
import json

from subfork.logger import log
from subfork.api.base import Base


def sanitize_data(data, default={}):
    """
    Validates data. Returns input data or an empty dict.

    :param data: data dict to sanitize
    :param default: default value if data is None
    """

    try:
        if data is None:
            data = default

        # data must be json serializable
        json.dumps(data)

        # data size limits
        assert sys.getsizeof(data) < 8192, "data too large"

        # data dict num keys limit
        if type(data) == dict:
            assert len(data.keys()) < 25, "too many keys"

    except AssertionError as err:
        log.warning(err)
        return {}

    except TypeError as err:
        log.warning("data is not json serializable: %s" % err)
        return {}

    return data


class Datatype(Base):
    """Subfork Datatype class."""

    def __init__(self, client, name):
        super(Datatype, self).__init__(client)
        self.name = name

    def __repr__(self):
        return "<Datatype %s>" % (self.name)

    @classmethod
    def get(cls, client, name):
        """
        Gets and returns a new Datatype object instance

        :param client: Subfork client instance
        :param: Datatype name
        """
        return cls(client, name)

    def batch(self):
        """Batch insert many rows for this datatype."""
        raise NotImplementedError

    def delete(self, params):
        """
        Deletes data rows from a given data collection matching
        a set of search params.

        :param params: dictionary of key/value data
        :returns: True if delete was successful
        """
        if not params:
            raise Exception("missing params")
        return self.client._request(
            "data/delete",
            data={
                "collection": self.name,
                "params": params,
            },
        )

    def find(self, params, expand=False, page=1, limit=100):
        """
        Query a data collection matching a given set of search params.
        Returns matching results up to a givem limit.

        :param params: list of search params, e.g.

            [[field1, "=", value1], [field2, ">", value2]]

            Supported operands:

                ">": greater than
                "<": less tahn
                ">=": greater than or equal
                "<=": less then or or equal
                "=": equal to
                "in": in a list
                "not_in": not in a list
                "!=": not equal to
                "~=": regex pattern matching

        :param expand: expand nested datatypes
        :param page: current page number
        :param limit: limit the query results
        :returns: list of results as data dicts
        """
        if not params:
            raise Exception("missing params")
        params = {
            "collection": self.name,
            "expand": expand,
            "limit": limit,
            "paging": {"current_page": page, "results_per_page": limit},
            "params": params,
        }
        return self.client._request("data/get", data=params)

    def find_one(self, params, expand=False):
        """
        Query a data collection matching a given set of search params.
        Returns at most one result.

        :param params: list of search params, e.g. ::

            [[field1, "=", value1], [field2, ">", value2]]

        :param expand: expand collection ids

        :returns: results as data dict
        """
        results = self.find(params, expand, page=1, limit=1)
        if results:
            return results[0]
        return

    def insert(self, data):
        """
        Inserts a new data into for this datatype.

        :param data: dictionary of key/value data
        :returns: inserted data dict
        """
        return self.client._request(
            "data/create",
            data={
                "collection": self.name,
                "data": sanitize_data(data),
                "upsert": False,
            },
        )

    def upsert(self, data):
        """
        Upserts a new data into for this datatype.

        :param data: dictionary of key/value data
        :returns: upserted data dict
        """
        return self.client._request(
            "data/create",
            data={
                "collection": self.name,
                "data": sanitize_data(data),
            },
        )
