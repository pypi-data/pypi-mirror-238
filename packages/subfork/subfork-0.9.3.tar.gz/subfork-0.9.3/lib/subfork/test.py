#!/usr/bin/env python
#
# Copyright (c) 2022-2023 Subfork. All rights reserved.
#

__doc__ = """
Contains subfork API unit tests.
"""

import os
import shutil
import tempfile
import unittest

from random import randint

from subfork import config
from subfork import util


class TestConfig(unittest.TestCase):
    """Tests the subfork.config module."""

    def test_import(self):
        from subfork import config

        self.assertTrue(os.path.exists(config.__file__))

    def test_read_config_file(self):
        from subfork import config

        filename = os.path.join(
            os.path.dirname(__file__), "..", "..", "example_config.yaml"
        )
        self.assertTrue(os.path.exists(filename))
        data = config.load_file(filename)
        self.assertTrue("DEBUG" in data)
        self.assertTrue("SUBFORK_HOST" in data)
        self.assertTrue("SUBFORK_PORT" in data)


class TestLogger(unittest.TestCase):
    """Tests the subfork.logger module."""

    def test_stream_handler(self):
        import logging
        from subfork.logger import log, setup_stream_handler

        setup_stream_handler()
        log.setLevel(logging.DEBUG)
        log.debug("test debug")
        log.info("test info")
        log.error("test error")
        log.warning("test warning")


class TestClient(unittest.TestCase):
    """Tests the subfork.client module."""

    def test_client(self):
        from subfork import get_client

        client = get_client()
        self.assertEqual(client.conn().host, config.HOST)
        self.assertEqual(client.conn().port, config.PORT)

    def test_shared_connection(self):
        from subfork import get_client

        c1 = get_client()
        c2 = get_client()

        self.assertEqual(c1.conn(), c2.conn())
        self.assertNotEqual(c1.conn().sessionid, None)
        self.assertNotEqual(c2.conn().sessionid, None)
        self.assertEqual(c1.conn().sessionid, c2.conn().sessionid)
        self.assertEqual(c1.site(), c2.site())


class TestApiData(unittest.TestCase):
    """Tests the subfork.api.data module."""

    client = None

    @classmethod
    def setUpClass(cls):
        from subfork import get_client

        cls.client = get_client()

    @classmethod
    def tearDownClass(cls):
        cls.client = None

    def test_basic_upsert_find_delete(self):
        """Tests basic upsert, find and delete functions."""
        test_data = self.client.get_data("test")
        self.assertTrue(test_data is not None)

        foo = randint(0, 1000)
        bar = randint(0, 1000)

        # create a new data row
        test1 = test_data.upsert({"foo": foo, "bar": bar, "this": "something"})
        self.assertTrue(test1 is not None)
        self.assertTrue("id" in test1)
        self.assertEqual(test1.get("foo"), foo)
        self.assertEqual(test1.get("bar"), bar)
        self.assertEqual(test1.get("this"), "something")

        # query the row back
        params = [["id", "=", test1.get("id")]]
        test2 = test_data.find_one(params)
        self.assertEqual(test2["id"], test1["id"])
        self.assertEqual(test2.get("foo"), foo)
        self.assertEqual(test2.get("bar"), bar)
        self.assertEqual(test2.get("this"), "something")

        results = test_data.find(params)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], test2)

        # delete the row
        success = test_data.delete(params)
        self.assertTrue(success)
        test = test_data.find_one(params)
        self.assertEqual(test, None)


class TestApiUser(unittest.TestCase):
    """Tests the subfork.api.user module."""

    client = None

    @classmethod
    def setUpClass(cls):
        from subfork import get_client

        cls.client = get_client()

    @classmethod
    def tearDownClass(cls):
        cls.client = None

    def test_create_user(self):
        username = "testuser%04d" % randint(0, 999)
        email = "%s@test.com" % username

        # test create user
        user = self.client.site().create_user(username=username, email=email)
        self.assertIsNotNone(user)
        self.assertEqual(user.data().get("username"), username)
        self.assertEqual(user.data().get("email"), email)

        # test get user
        user = self.client.get_user(username=username)
        self.assertIsNotNone(user)
        self.assertEqual(user.data().get("username"), username)
        self.assertEqual(user.data().get("email"), email)

        # disable test user
        disabled = user.disable()
        self.assertTrue(disabled)


class TestUtils(unittest.TestCase):
    """Tests the subfork.utils module."""

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tempdir)

    def test_b2h(self):
        """Tests bytes to human b2h() function."""
        self.assertEqual(util.b2h(1024), "1.0K")
        self.assertEqual(util.b2h(2048), "2.0K")
        self.assertEqual(util.b2h(4608), "4.5K")
        self.assertEqual(util.b2h(1048576), "1.0M")
        self.assertEqual(util.b2h(5242880), "5.0M")
        self.assertEqual(util.b2h(10485760), "10.0M")

    def test_check_version(self):
        """Tests pypi check_version() function."""
        self.assertTrue(util.check_version())

    def test_checksum(self):
        """Tests checksum() function."""
        filename = os.path.join(
            os.path.dirname(__file__), "..", "..", "example_config.yaml"
        )
        value = util.checksum(filename)
        self.assertTrue(value is not None)

    def test_gettime(self):
        """Tests gettime() function."""
        import time

        t = util.get_time()
        self.assertEqual(t, int(time.time() * 1000.0))

    def test_ignorables(self):
        """Tests is_ignorable() function."""
        self.assertTrue(util.is_ignorable(".this_is_ignorable"))
        self.assertTrue(util.is_ignorable("temp-file.tmp"))
        self.assertTrue(util.is_ignorable("script.php"))
        self.assertTrue(util.is_ignorable("test.py"))
        self.assertTrue(util.is_ignorable("test.pyc"))
        self.assertTrue(util.is_ignorable("lib.so"))

    def test_minify(self):
        """Tests js minify() function."""
        pass


if __name__ == "__main__":
    unittest.main()
