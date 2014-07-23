import unittest
from mock import patch, sentinel
import sys

import combine_rebrickable_csv

class TestCombineRebrickableCsv(unittest.TestCase):

    @patch('low_level.write_csv_file')
    @patch('combine_rebrickable_csv.combine')
    @patch('low_level.read_csv_file')
    def test_combine_rebrickable_csv(self, read_csv_file_mock, combine_mock, write_csv_file_mock):
        # Setup
        file1 = 'file1.csv'
        file2 = 'file2.csv'
        csv_files = [file1, file2]
        file1_rows = [['Part', 'Color', 'Num'], ['a', 'b'], ['c', 'd'], ['y', 'z']]
        file2_rows = [['Part', 'Color', 'Num'], ['e', 'f'], ['g', 'h'], ['1', '2']]
        output_file = 'combined.csv'
        read_csv_file_mock.side_effect = lambda x: {file1: file1_rows, file2: file2_rows}[x]
        combine_mock.return_value = sentinel.combined_parts

        # Call method-under-test
        combine_rebrickable_csv.combine_rebrickable_csv(csv_files, output_file)

        # Verification
        list_of_list_of_parts = [file1_rows[1:], file2_rows[1:]]
        combine_mock.assert_called_once_with(list_of_list_of_parts)
        write_csv_file_mock.assert_called_once_with(output_file, sentinel.combined_parts, header=['Part', 'Color', 'Num'])

    @patch('low_level.write_csv_file')
    @patch('combine_rebrickable_csv.combine')
    @patch('low_level.read_csv_file')
    def test_combine_rebrickable_csv_bad_file(self, read_csv_file_mock, combine_mock, write_csv_file_mock):
        # Setup
        file1 = 'file1.csv'
        file2 = 'file2.csv'
        csv_files = [file1, file2]
        file1_rows = [['a', 'b'], ['c', 'd'], ['y', 'z']]
        file2_rows = [['Part', 'Color', 'Num'], ['e', 'f'], ['g', 'h'], ['1', '2']]
        output_file = 'combined.csv'
        read_csv_file_mock.side_effect = lambda x: {file1: file1_rows, file2: file2_rows}[x]

        # Call method-under-test
        self.assertRaises(Exception, combine_rebrickable_csv.combine_rebrickable_csv, csv_files, output_file)
        self.assertFalse(combine_mock.called)
        self.assertFalse(write_csv_file_mock.called)

    def test_combine(self):
        # Setup
        list_of_list_of_parts = [
            [['1234', '0', '13',],
             ['5678', '5', '17',],
             ['1234', '0', '19',],],
            [['4532', '6', '13',],
             ['5678', '5', '29',],
             ['1234', '50', '1',],
             ['8373', '0', '2',],],
        ]

        # Call method-under-test
        ret = combine_rebrickable_csv.combine(list_of_list_of_parts)

        # Verification
        expected = [
                ['1234', '0', '32',],
                ['5678', '5', '46',],
                ['4532', '6', '13',],
                ['1234', '50', '1',],
                ['8373', '0', '2',],]
        self.assertEqual(ret, expected)

    @patch('combine_rebrickable_csv.combine_rebrickable_csv')
    def test_main(self, combine_rebrickable_csv_mock):
        # Setup
        sys.argv = ['./combine_rebrickable_csv.py', 'file1.csv', 'file2.csv']

        # Call method-under-test
        combine_rebrickable_csv.main()

        # Verification
        combine_rebrickable_csv_mock.assert_called_once_with(['file1.csv', 'file2.csv'], 'combined.csv')
