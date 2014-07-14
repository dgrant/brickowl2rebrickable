import urllib.request

import rebrickable_colors
import low_level

class Rebrickable(object):

    def __init__(self):
        self._color_table = None

    def get_color_id_from_brick_owl_name(self, brickowl_name):
        if self._color_table is None:
            self._color_table = self._get_color_conversion_table()
        return self._color_table.get_color_id_from_brick_owl_name(brickowl_name)

    def _get_color_conversion_table(self):
        html = low_level.do_http_get('http://rebrickable.com/colors')
        parser = rebrickable_colors.ColorTableParser()
        parser.feed(html)
        table_data = parser.table_data
        return rebrickable_colors.ColorTable(table_data)