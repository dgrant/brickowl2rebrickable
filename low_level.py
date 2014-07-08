import urllib.parse
import urllib.request

__author__ = 'david'

def do_http_get(url, params=None):
    """
    Perform an http get, returning the response data.

    :param url: full url including protocol and port
    :param params: dictionary of parameters
    :return: the body of the HTTP response
    """
    if params is not None:
        url = (url + '?%s') % urllib.parse.urlencode(params)
    f = urllib.request.urlopen(url)
    return f.read().decode('utf8')