import unittest
from mock import Mock
import urllib.request

from converter import BrickOwl

class TestBrickOwl(unittest.TestCase):
    def setUp(self):
        self.brickOwl = BrickOwl("API_KEY")

    def test_fetch_order(self):
        # Setup
        handle_mock = Mock()
        urllib.request.urlopen = Mock(return_value=handle_mock)

        # Call method-under-test
        self.brickOwl.fetch_order(1)

        # Verification
        urllib.request.urlopen.assert_called_once_with("https://api.brickowl.com/v1/order/items?order_id=1&key=API_KEY")
