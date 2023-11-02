"""Test misc utility functions"""
from requests.exceptions import RetryError

from .helpers import APITestCase

from sermonaudio import create_or_configure_session_with_retry
from sermonaudio.utils import update_kwargs_for_key


class UtilsTests(APITestCase):
    def test_session_retry(self):
        session = create_or_configure_session_with_retry(retries=5)

        try:
            # Make sure that a known bad request will never succeed
            session.get("http://httpbin.org/status/500")
        except RetryError:
            pass
        else:
            self.assertEqual(True, False, "Should have not succeeded")

        # Make sure it eventually succeeds (it should with this many retry chances haha)
        response = session.get("http://httpbin.org/status/500,200")
        self.assertEqual(response.status_code, 200)

    def test_update_kwargs_for_key_func(self):
        # Empty kwargs
        kwargs = {}
        update_kwargs_for_key(kwargs, "foo", {"bar": "baz"})

        self.assertEqual(kwargs, {"foo": {"bar": "baz"}})

        # kwargs with irrelevant key that shouldn't be touched
        kwargs = {"qux": "quux"}
        update_kwargs_for_key(kwargs, "foo", {"bar": "baz"})

        self.assertEqual(kwargs, {"qux": "quux", "foo": {"bar": "baz"}})

        # kwargs with existing dict for key
        kwargs = {"foo": {"qux": "quux"}}

        update_kwargs_for_key(kwargs, "foo", {"bar": "baz"})

        self.assertEqual(kwargs, {"foo": {"bar": "baz", "qux": "quux"}})

        # kwargs with existing dict for key and value that will be replaced
        kwargs = {"foo": {"bar": "quux"}}
        update_kwargs_for_key(kwargs, "foo", {"bar": "baz"})

        self.assertEqual(kwargs, {"foo": {"bar": "baz"}})
