import _io
import unittest
import brickowl2rebrickable_conf

from mock import patch, MagicMock

def mock_open(mock=None, read_data='', lines=None):
    """
    A helper function to create a mock to replace the use of `open`. It works
    for `open` called directly or used as a context manager.

    The `mock` argument is the mock object to configure. If `None` (the
    default) then a `MagicMock` will be created for you, with the API limited
    to methods or attributes available on standard file handles.

    `read_data` is a string for the `read` method of the file handle to return.
    This is an empty string by default.
    """
    file_spec = list(set(dir(_io.TextIOWrapper)).union(set(dir(_io.BytesIO))))

    mock = MagicMock(name='open', spec=open)

    handle = MagicMock(spec=file_spec)
    handle.__enter__.return_value = handle
    handle.read.return_value = read_data
    if lines is not None:
        handle.__iter__.return_value = iter(lines)

    mock.return_value = handle
    return mock


class TestBrickOwl2RebrickableConf(unittest.TestCase):

    def test_get_brickowl_api_key_no_key(self):
        m = mock_open()
        with patch('builtins.open', m, create=True):
            ret = brickowl2rebrickable_conf.get_brickowl_api_key()
            self.assertEqual(ret, None)

    def test_get_brickowl_api_key(self):
        lines = ['[DEFAULT]', 'BrickOwlApiKey = e70ed76dae2a9eb1869e4b1ea88ac2b4221ae94fc05e3a8a0e58f41614924f47']

        m = mock_open(lines=lines)
        with patch('builtins.open', m, create=True):
            ret = brickowl2rebrickable_conf.get_brickowl_api_key()
            self.assertEqual(ret, 'e70ed76dae2a9eb1869e4b1ea88ac2b4221ae94fc05e3a8a0e58f41614924f47')