import collections
import unittest
from mock import patch, Mock, mock_open, call

from low_level import do_http_get, write_csv_file

class TestLowLevel(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_do_http_get(self, urlopen_mock):
        # setup
        url = 'http://www.google.ca'
        http_response_string = 'response'
        urlopen_mock.return_value.read.return_value.decode.return_value = http_response_string

        # call method-under-test
        ret = do_http_get(url)

        # verify
        urlopen_mock.assert_called_once_with(url)
        urlopen_mock.return_value.read.return_value.decode.assert_called_once_with('utf8')
        self.assertEqual(ret, http_response_string)

    @patch('urllib.request.urlopen')
    def test_do_http_get_with_params(self, urlopen_mock):
        # setup
        url = 'http://www.google.ca'
        http_response_string = 'response'
        params = collections.OrderedDict()
        params['a'] = 1
        params['b'] = 2
        params['c'] = 3
        urlopen_mock.return_value.read.return_value.decode.return_value = http_response_string

        # call method-under-test
        ret = do_http_get(url, params)

        # verify
        urlopen_mock.assert_called_once_with(url + "?a=1&b=2&c=3")
        urlopen_mock.return_value.read.return_value.decode.assert_called_once_with('utf8')
        self.assertEqual(ret, http_response_string)

    @patch('csv.writer')
    def test_write_csv_file(self, csv_writer_mock):
        rows = [['a', 'b'], ['c', 'd']]
        m = mock_open()
        with patch('low_level.open', m, create=True):
            write_csv_file('filename', rows)

            m.assert_called_with('filename', 'w')
            #handle = m()
            #csv_writer_mock.assert_called_once_with(handle, delimeter=',')
            expected_calls = [call(['a', 'b']), call(['c', 'd'])]
            writer = csv_writer_mock.return_value
            self.assertEqual(writer.writerow.call_args_list, expected_calls)

    @patch('csv.writer')
    def test_write_csv_file_with_header(self, csv_writer_mock):
        rows = [['a', 'b'], ['c', 'd']]
        header = ['head', 'er']
        m = mock_open()
        with patch('low_level.open', m, create=True):
            write_csv_file('filename', rows, header=header)

            m.assert_called_with('filename', 'w')
            #handle = m()
            #csv_writer_mock.assert_called_once_with(handle, delimeter=',')
            expected_calls = [call(['head', 'er']), call(['a', 'b']), call(['c', 'd'])]
            writer = csv_writer_mock.return_value
            self.assertEqual(writer.writerow.call_args_list, expected_calls)

if __name__ == '__main__':
    unittest.main()