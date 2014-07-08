import unittest
import mock
from mock import Mock, MagicMock
import urllib.request
from urllib.parse import urlparse

import converter

class Matcher(object):
    def __init__(self, compare, some_obj):
        self.compare = compare
        self.some_obj = some_obj

    def __eq__(self, other):
        return self.compare(self.some_obj, other)

def compare(first, second):
    first = urlparse(first)
    second = urlparse(second)
    if first.scheme == second.scheme \
        and first.netloc == second.netloc \
        and first.path == second.path \
        and first.params == second.params \
        and first.query == second.query:
        return True
    else:
        return False

class TestBrickOwl(unittest.TestCase):
    def setUp(self):
        self.brickOwl = converter.BrickOwl("API_KEY")

    def test_fetch_order(self):
        # Setup
        converter.do_http_get = Mock(return_value="['some json here']")

        # Call method-under-test
        self.brickOwl.fetch_order(1)

        # Verification
        converter.do_http_get.assert_called_once_with("https://api.brickowl.com/v1/order/items", {'order_id': 1, 'key': 'API_KEY'})
