import unittest
from mock import Mock, MagicMock

import low_level
import brickowl

class TestBrickOwl(unittest.TestCase):
    def setUp(self):
        self.brickOwl = brickowl.BrickOwl("API_KEY")

    def test_fetch_order(self):
        # Setup
        low_level.do_http_get = Mock(return_value="['some json here']")

        # Call method-under-test
        self.brickOwl.fetch_order(1)

        # Verification
        low_level.do_http_get.assert_called_once_with("https://api.brickowl.com/v1/order/items", {'order_id': 1, 'key': 'API_KEY'})
