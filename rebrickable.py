import urllib.request

from rebrickable_colors import ColorTableParser, ColorTable
from low_level import do_http_get

class Rebrickable(object):

    def __init__(self):
        self._color_table = None

    def get_color_id_from_brick_owl_name(self, brickowl_name):
        if self._color_table is None:
            self._color_table = self._get_color_conversion_table()
        return self._color_table.get_color_id_from_brick_owl_name(brickowl_name)

    def _get_color_conversion_table(self):
        print("got here")
        html = do_http_get('http://rebrickable.com/colors')
        parser = ColorTableParser()
        parser.feed(html)
        return ColorTable(parser.table_data)