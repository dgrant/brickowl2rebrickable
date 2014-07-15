import unittest
import sys

from mock import patch

import brickowl2rebrickable
import brickowl2rebrickable_conf


class TestBrickOwl2Rebrickable(unittest.TestCase):

    @patch('brickowl.BrickOwl')
    def test_brickowl2rebrickable(self, BrickOwlMock):
        # Setup
        api_key = 'kdajfljdlk'
        orders = ['1', '2']

        # Call method-under-test
        brickowl2rebrickable.brickowl2rebrickable(api_key, orders)

        # Verification
        BrickOwlMock.assert_called_once_with(api_key)
        BrickOwlMock.return_value.export_to_rebrickable_csvs.assert_called_once_with(orders,
                                                                output_dir=brickowl2rebrickable.DEFAULT_OUTPUTDIR)

    @patch('brickowl.BrickOwl')
    def test_brickowl2rebrickable_with_outputdir(self, BrickOwlMock):
        # Setup
        api_key = 'kdajfljdlk'
        orders = ['1', '2']
        output_dir = 'blather'

        # Call method-under-test
        brickowl2rebrickable.brickowl2rebrickable(api_key, orders, output_dir=output_dir)

        # Verification
        BrickOwlMock.assert_called_once_with(api_key)
        BrickOwlMock.return_value.export_to_rebrickable_csvs.assert_called_once_with(orders, output_dir=output_dir)

    @patch('brickowl2rebrickable_conf.get_brickowl_api_key')
    @patch('brickowl.BrickOwl')
    def test_brickowl2rebrickable_with_apikey_from_file(self, BrickOwlMock, get_api_key_mock):
        # Setup
        api_key = 'kdajfljdlk'
        orders = ['1', '2']
        output_dir = 'blather'
        get_api_key_mock.return_value = api_key

        # Call method-under-test
        brickowl2rebrickable.brickowl2rebrickable(None, orders, output_dir=output_dir)

        # Verification
        BrickOwlMock.assert_called_once_with(api_key)
        BrickOwlMock.return_value.export_to_rebrickable_csvs.assert_called_once_with(orders, output_dir=output_dir)

    @patch('brickowl2rebrickable_conf.get_brickowl_api_key')
    @patch('brickowl.BrickOwl')
    def test_brickowl2rebrickable_with_apikey_from_file_commandline_override(self, BrickOwlMock, get_api_key_mock):
        # Setup
        api_key = 'kdajfljdlk'
        api_key_from_file = 'ajflkdajfkl'
        orders = ['1', '2']
        output_dir = 'blather'
        get_api_key_mock.return_value = api_key

        # Call method-under-test
        brickowl2rebrickable.brickowl2rebrickable(api_key_from_file, orders, output_dir=output_dir)

        # Verification
        BrickOwlMock.assert_called_once_with(api_key_from_file)
        BrickOwlMock.return_value.export_to_rebrickable_csvs.assert_called_once_with(orders, output_dir=output_dir)

    @patch('brickowl2rebrickable_conf.get_brickowl_api_key')
    @patch('brickowl.BrickOwl')
    def test_brickowl2rebrickable_no_apikey(self, BrickOwlMock, get_api_key_mock):
        # Setup
        orders = ['1', '2']
        output_dir = 'blather'
        get_api_key_mock.return_value = None

        # Call method-under-test
        self.assertRaises(Exception, brickowl2rebrickable.brickowl2rebrickable, None, orders, output_dir=output_dir)

        # Verification
        self.assertFalse(BrickOwlMock.called)

    @patch('brickowl2rebrickable.brickowl2rebrickable')
    def test_main(self, brickowl2rebrickable_mock):
        # Setup
        sys.argv = ['./brickowl2rebrickable.py', '8827569', '1234']

        # Call method-under-test
        brickowl2rebrickable.main()

        # Verification
        brickowl2rebrickable_mock.assert_called_once_with(None, ['8827569', '1234'])

    @patch('brickowl2rebrickable.brickowl2rebrickable')
    def test_main_with_api_key(self, brickowl2rebrickable_mock):
        # Setup
        api_key = 'api_key'
        sys.argv = ['./brickowl2rebrickable.py', '-b', api_key, '1234']

        # Call method-under-test
        brickowl2rebrickable.main()

        # Verification
        brickowl2rebrickable_mock.assert_called_once_with(api_key, ['1234'])

