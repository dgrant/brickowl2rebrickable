import csv
import hashlib
import urllib.parse
import urllib.request


def do_http_get(url, params=None):
    """
    Perform an http get, returning the response data.

    :param url: full url including protocol and port
    :param params: dictionary of parameters
    :return: the body of the HTTP response
    """
    if params is not None:
        url = (url + '?%s') % urllib.parse.urlencode(params)
    # print('url=', url)
    url_handle = urllib.request.urlopen(url)
    return url_handle.read().decode('utf8')


def write_csv_file(filename, rows, header=None):
    with open(filename, 'w') as handle:
        writer = csv.writer(handle, delimiter=',')
        if header is not None:
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def md5sum_file(filename):
    md5sum = hashlib.md5()
    with open(filename) as file_handle:
        for line in file_handle:
            md5sum.update(line.encode('utf8'))
    return md5sum.digest()
