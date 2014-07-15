import unittest
import sys

from mock import patch

import brickowl2rebrickable
import brickowl2rebrickable_conf


class TestBrickOwl2Rebrickable(unittest.TestCase):

    @patch('brickowl.BrickOwl')
    def test_brickowl2rebrickable(self, BrickOwlMock):
        # Setup
        brickowl_api_key = 'kdajfljdlk'
        rebrickable_api_key = 'ldalkjfda'
        orders = ['1', '2']

        # Call method-under-test
        brickowl2rebrickable.brickowl2rebrickable(brickowl_api_key, rebrickable_api_key, orders)

        # Verification
        BrickOwlMock.assert_called_once_with(brickowl_api_key, rebrickable_api_key)
        BrickOwlMock.return_value.export_to_rebrickable_csvs.assert_called_once_with(orders,
                                                                output_dir=brickowl2rebrickable.DEFAULT_OUTPUTDIR)

    @patch('brickowl.BrickOwl')
    def test_brickowl2rebrickable_with_outputdir(self, BrickOwlMock):
        # Setup
        brickowl_api_key = 'kdajfljdlk'
        rebrickable_api_key = 'lklkja'
        orders = ['1', '2']
        output_dir = 'blather'

        # Call method-under-test
        brickowl2rebrickable.brickowl2rebrickable(brickowl_api_key, rebrickable_api_key, orders, output_dir=output_dir)

        # Verification
        BrickOwlMock.assert_called_once_with(brickowl_api_key, rebrickable_api_key)
        BrickOwlMock.return_value.export_to_rebrickable_csvs.assert_called_once_with(orders, output_dir=output_dir)

    @patch('brickowl2rebrickable_conf.get_rebrickable_api_key')
    @patch('brickowl2rebrickable_conf.get_brickowl_api_key')
    @patch('brickowl.BrickOwl')
    def test_brickowl2rebrickable_with_apikey_from_file(self, BrickOwlMock, get_brickowl_api_key_mock, get_rebrickable_api_key_mock):
        # Setup
        brickowl_api_key = 'kdajfljdlk'
        rebrickable_api_key = 'afdalk'
        orders = ['1', '2']
        output_dir = 'blather'
        get_brickowl_api_key_mock.return_value = brickowl_api_key
        get_rebrickable_api_key_mock.return_value = rebrickable_api_key

        # Call method-under-test
        brickowl2rebrickable.brickowl2rebrickable(None, None, orders, output_dir=output_dir)

        # Verification
        BrickOwlMock.assert_called_once_with(brickowl_api_key, rebrickable_api_key)
        BrickOwlMock.return_value.export_to_rebrickable_csvs.assert_called_once_with(orders, output_dir=output_dir)

    @patch('brickowl2rebrickable_conf.get_rebrickable_api_key')
    @patch('brickowl2rebrickable_conf.get_brickowl_api_key')
    @patch('brickowl.BrickOwl')
    def test_brickowl2rebrickable_with_apikey_from_file_commandline_override(self, BrickOwlMock, get_brickowl_api_key_mock, get_rebrickable_api_key_mock):
        # Setup
        brickowl_api_key = 'kdajfljdlk'
        brickowl_api_key_from_file = 'ajflkdajfkl'
        rebrickable_api_key = '234324'
        rebrickable_api_key_from_file = '11111'
        orders = ['1', '2']
        output_dir = 'blather'
        get_brickowl_api_key_mock.return_value = brickowl_api_key_from_file
        get_rebrickable_api_key_mock.return_value = rebrickable_api_key_from_file

        # Call method-under-test
        brickowl2rebrickable.brickowl2rebrickable(brickowl_api_key, rebrickable_api_key, orders, output_dir=output_dir)

        # Verification
        BrickOwlMock.assert_called_once_with(brickowl_api_key, rebrickable_api_key)
        BrickOwlMock.return_value.export_to_rebrickable_csvs.assert_called_once_with(orders, output_dir=output_dir)

    @patch('brickowl2rebrickable_conf.get_rebrickable_api_key')
    @patch('brickowl2rebrickable_conf.get_brickowl_api_key')
    @patch('brickowl.BrickOwl')
    def test_brickowl2rebrickable_no_apikeys(self, BrickOwlMock, get_brickowl_api_key_mock, get_rebrickable_api_key_mock):
        # Setup
        orders = ['1', '2']
        output_dir = 'blather'
        get_brickowl_api_key_mock.return_value = None
        get_rebrickable_api_key_mock.return_value = None

        # Call method-under-test
        self.assertRaises(Exception, brickowl2rebrickable.brickowl2rebrickable, None, None, orders, output_dir=output_dir)

        # Verification
        self.assertFalse(BrickOwlMock.called)

    @patch('brickowl2rebrickable.brickowl2rebrickable')
    def test_main(self, brickowl2rebrickable_mock):
        # Setup
        sys.argv = ['./brickowl2rebrickable.py', '8827569', '1234']

        # Call method-under-test
        brickowl2rebrickable.main()

        # Verification
        brickowl2rebrickable_mock.assert_called_once_with(None, None, ['8827569', '1234'])

    @patch('brickowl2rebrickable.brickowl2rebrickable')
    def test_main_with_api_keys(self, brickowl2rebrickable_mock):
        # Setup
        brickowl_api_key = 'brickowl_api_key'
        rebrickable_api_key = 'rebrickable_api_key'
        sys.argv = ['./brickowl2rebrickable.py', '-b', brickowl_api_key, '-r', rebrickable_api_key, '1234']

        # Call method-under-test
        brickowl2rebrickable.main()

        # Verification
        brickowl2rebrickable_mock.assert_called_once_with(brickowl_api_key, rebrickable_api_key, ['1234'])

