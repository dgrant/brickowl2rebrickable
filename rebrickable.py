import json

import collections
import functools
import rebrickable_colors
import low_level

def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer

class Rebrickable(object):

    def __init__(self, api_key):
        self._color_table = None
        self.api_key = api_key

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

    @memoize
    def _get_num_parts(self, _id):
        result = low_level.do_http_get('http://rebrickable.com/api/get_part', params=collections.OrderedDict({'key': self.api_key, 'part_id': _id, 'format': 'json'}))

        num_parts = 0
        if result != 'NOPART':
            result_json = json.loads(result)
            for color in result_json['colors']:
                num_parts += int(color['num_parts'])
        return num_parts

    def get_best_part_match(self, ids):
        best_part = None
        best_total_parts = 0
        for _id in ids:
            num_parts = self._get_num_parts(_id)
            if num_parts > best_total_parts:
                best_total_parts = num_parts
                best_part = _id
        return best_part
