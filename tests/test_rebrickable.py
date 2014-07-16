import unittest

from mock import patch, Mock, sentinel, call

import rebrickable

class TestRebrickable(unittest.TestCase):

    def setUp(self):
        self.rebrickable = rebrickable.Rebrickable('API_KEY')

    def test_get_color_conversion_table(self):
        # Setup
        mock_color_table = Mock()
        self.rebrickable._get_color_conversion_table = Mock(return_value = mock_color_table)

        # Call method-under-test
        self.rebrickable.get_colorid_from_brickowl_name('White')

        # Verification
        mock_color_table.get_colorid_from_brickowl_name.assert_called_once_with('White')

    def test_get_color_conversion_table_table_cached(self):
        # Setup
        mock_color_table = Mock()
        self.rebrickable._color_table = mock_color_table

        # Call method-under-test
        self.rebrickable.get_colorid_from_brickowl_name('White')

        # Verification
        mock_color_table.get_colorid_from_brickowl_name.assert_called_once_with('White')

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

    @patch('low_level.do_http_get')
    def test_get_best_part_match(self, do_http_get_mock):
        # Setup
        api_url = 'http://rebrickable.com/api/get_part'
        results = {'1': '{"part_id":"1","colors":[{"ldraw_color_id":"0","color_name":"Black","num_sets":"1025","num_parts":"100"},{"ldraw_color_id":"1","color_name":"Blue","num_sets":"530","num_parts":"50"}]}',
                   '2': '{"part_id":"2","colors":[{"ldraw_color_id":"0","color_name":"Black","num_sets":"1025","num_parts":"100"},{"ldraw_color_id":"1","color_name":"Blue","num_sets":"530","num_parts":"200"}]}',
                   'invalid part num': 'NOPART'}
        def result(*args, **kwargs):
            return results[kwargs['params']['part_id']]

        do_http_get_mock.side_effect = result

        # Call method-under-test
        self.rebrickable.get_best_part_match(['1', '2', 'invalid part num'])
        best_part = self.rebrickable.get_best_part_match(['1', '2', 'invalid part num']) # Calling again shouldn't increase number of http calls as it is memoized

        # Verification
        self.assertEqual(do_http_get_mock.mock_calls, [call(api_url, params={'key': 'API_KEY', 'part_id': '1', 'format': 'json'}),
                                                       call(api_url, params={'key': 'API_KEY', 'part_id': '2', 'format': 'json'}),
                                                       call(api_url, params={'key': 'API_KEY', 'part_id': 'invalid part num', 'format': 'json'})])
        self.assertEqual(best_part, '2')
