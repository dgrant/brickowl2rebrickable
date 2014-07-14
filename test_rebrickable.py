import unittest

from mock import patch, Mock, sentinel
from numpy.f2py.auxfuncs import l_and

import rebrickable

class TestRebrickable(unittest.TestCase):

    def setUp(self):
        self.rebrickable = rebrickable.Rebrickable()

    def test_get_color_conversion_table(self):
        # Setup
        mock_color_table = Mock()
        self.rebrickable._get_color_conversion_table = Mock(return_value = mock_color_table)

        # Call method-under-test
        self.rebrickable.get_color_id_from_brick_owl_name('White')

        # Verification
        mock_color_table.get_color_id_from_brick_owl_name.assert_called_once_with('White')

    def test_get_color_conversion_table_table_cached(self):
        # Setup
        mock_color_table = Mock()
        self.rebrickable._color_table = mock_color_table

        # Call method-under-test
        self.rebrickable.get_color_id_from_brick_owl_name('White')

        # Verification
        mock_color_table.get_color_id_from_brick_owl_name.assert_called_once_with('White')

    @patch('rebrickable_colors.ColorTable')
    @patch('rebrickable_colors.ColorTableParser')
    @patch('low_level.do_http_get')
    def test__get_color_conversion_table(self, do_http_get_mock, ColorTableParser_mock, ColorTable_mock):
        # Setup
        do_http_get_mock.return_value = sentinel.html
        color_table_parser = ColorTableParser_mock.return_value
        color_table_parser.table_data = sentinel.table_data
        color_table = ColorTable_mock.return_value

        # Call method-under-test
        ret = self.rebrickable._get_color_conversion_table()

        # Verification
        ColorTable_mock.assert_called_once_with(sentinel.table_data)
        color_table_parser.feed.assert_called_once_with(sentinel.html)
        self.assertEqual(ret, color_table)