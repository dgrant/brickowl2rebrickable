import unittest
import mock
from mock import Mock
import urllib.request
from urllib.parse import urlparse

from converter import BrickOwl

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
        self.brickOwl = BrickOwl("API_KEY")

    @mock.patch('urllib.request')
    def test_fetch_order(self, mock_request):
        # Setup
        handle_mock = Mock()
        mock_request.return_value = handle_mock

        # Call method-under-test
        self.brickOwl.fetch_order(1)

        # Verification
        matcher = Matcher(compare, "https://api.brickowl.com/v1/order/items?order_id=1&key=API_KEY")
        urllib.request.urlopen.assert_called_once_with(matcher)
