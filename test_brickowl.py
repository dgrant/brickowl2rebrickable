import unittest
from mock import Mock, MagicMock, patch

import low_level
import brickowl

class TestBrickOwl(unittest.TestCase):
    def setUp(self):
        self.brickOwl = brickowl.BrickOwl("API_KEY")

    @patch('low_level.do_http_get')
    def test_fetch_order(self, do_http_get_mock):
        # Setup
        json = "['some json here']"
        do_http_get_mock.return_value = json

        # Call method-under-test
        ret = self.brickOwl.fetch_order(1)

        # Verification
        low_level.do_http_get.assert_called_once_with("https://api.brickowl.com/v1/order/items", {'order_id': 1, 'key': 'API_KEY'})
        self.assertEqual(ret, json)
