"""
Rebrickable API.
"""
import json

import collections
import rebrickable_colors
import low_level


def get_color_conversion_table():
    """
    :return: a ColorTable object, parsed from http://rebrickable.com/colors
    """
    html = low_level.do_http_get('http://rebrickable.com/colors')
    parser = rebrickable_colors.ColorTableParser()
    parser.feed(html)
    table_data = parser.table_data
    return rebrickable_colors.ColorTable(table_data)


class Rebrickable(object):
    """
    Rebrickable API.
    """

    def __init__(self, api_key):
        self._color_table = None
        self.api_key = api_key

    def get_colorid_from_brickowl_name(self, brickowl_name):
        """
        Given a color name from BrickOwl, return a Rebrickable color_id

        :param brickowl_name: the BrickOwl color name
        :return: a Rebrickable color_id
        """
        if self._color_table is None:
            self._color_table = get_color_conversion_table()
        return self._color_table.get_colorid_from_brickowl_name(brickowl_name)

    @low_level.memoize
    def _get_num_parts(self, part_id):
        """
        Return the total number of parts found on Rebrickable.com for the part id
        :param part_id: a lego part id
        :return: the total number of parts found for the given part id
        """
        result = low_level.do_http_get('http://rebrickable.com/api/get_part',
                                       params=collections.OrderedDict(
                                           {'key': self.api_key, 'part_id': part_id, 'format': 'json'}))

        num_parts = 0
        if result != 'NOPART':
            result_json = json.loads(result)
            for color in result_json['colors']:
                num_parts += int(color['num_parts'])
        return num_parts

    def get_best_part_match(self, part_ids):
        """
        Finds the part number with the most parts on Rebrickable.com.

        :param part_ids: a list of lego part ids
        :return: the part number with the most number of parts found
        """
        best_part = None
        best_total_parts = 0
        for _id in part_ids:
            num_parts = self._get_num_parts(_id)
            if num_parts > best_total_parts:
                best_total_parts = num_parts
                best_part = _id
        return best_part
