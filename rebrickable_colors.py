"""
Parses rebrickable's color data from http://rebrickable.com/colors
"""

import html.parser


def strarray(data):
    """
    Parses a string that looks like '{foo, "bar"}' into an array of strings

    :param data: a string that look like '{foo, "bar"}' or '{foo, bar}', etc...
    :return: an array of string objects
    """
    data = data.strip('{}')
    data = data.split(',')
    data = [x.strip('"') for x in data]
    return data


def intarray(data):
    """
    Parses a string that looks like '{1, "2"}' into an array of ints

    :param data: a string that look like '{1, "2"}' or '{1, 2}', etc...
    :return: an array of int objects
    """
    return [int(x) for x in strarray(data)]


class ColorTableParser(html.parser.HTMLParser):  # pylint: disable=R0904
    """
    Parses the color data from http://rebrickable.com/colors
    """

    TYPES = {'ID': int,
             'Name': str,
             'RGB': str,
             'Num Parts': int,
             'Num Sets': int,
             'From Year': int,
             'To Year': int,
             'LEGO Color': strarray,
             'LDraw Color': intarray,
             'BrickLink Color': intarray,
             'Peeron Color': strarray}

    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self._in = {'table': False, 'row': False, 'col': False, 'header': False}
        self._row = 0
        self._col = 0
        self._header_data = {}
        self._row_data = None
        self.table_data = []

    def handle_starttag(self, tag, attrs):
        if not self._in['table'] and tag.lower() == 'table' and ('class', 'table') in attrs:
            self._in['table'] = True
        elif self._in['table']:
            if not self._in['row'] and tag.lower() == 'tr':
                self._in['row'] = True
                self._row_data = {}
            elif self._in['row'] and not self._in['col'] and tag.lower() == 'td':
                self._in['col'] = True

    def handle_endtag(self, tag):
        if tag.lower() == 'table':
            self._in['table'] = False
        elif tag.lower() == 'td':
            self._in['col'] = False
            self._col += 1
        elif tag.lower() == 'tr':
            self._in['row'] = False
            self._row += 1
            self._col = 0
            if not self._in['header']:
                self.table_data.append(self._row_data)
            else:
                self._in['header'] = False
            self._row_data = None

    def handle_data(self, data):
        if self._in['row'] and self._in['col']:
            if data == 'ID':
                self._in['header'] = True
                self._row -= 1

            if self._in['header']:
                self._header_data[self._col] = data
            else:
                header_name = self._header_data[self._col]
                self._row_data[header_name] = self.TYPES[header_name](data)


class ColorTable(object):
    """
    A table of color ids, parsed from http://rebrickable.com/colors
    """

    def __init__(self, data):
        self._data = data
        self._lego_color_to_id = {}
        self._peeron_color_to_id = {}
        self._color_name_to_id = {}
        self.parse()

    def parse(self):
        """
        Parse the data in self._data into a few maps that can be used to find a rebrickable id from another type of
        id such as lego color, peeron color, or Rebrickable color name

        :return: nothing
        """
        for color in self._data:
            if 'LEGO Color' in color:
                for lego_color_name in color['LEGO Color']:
                    self._lego_color_to_id[lego_color_name.lower()] = color['ID']
            if 'Peeron Color' in color:
                for peeron_color_name in color['Peeron Color']:
                    self._peeron_color_to_id[peeron_color_name.lower()] = color['ID']
            if 'Name' in color:
                self._color_name_to_id[color['Name'].lower()] = color['ID']

    def get_colorid_from_brickowl_name(self, brickowl_colorname):
        """
        :param brickowl_colorname: a brickowl color name
        :return: the Rebrickable color id for a brickowl color name
        """
        brickowl_colorname = brickowl_colorname.lower()
        if brickowl_colorname in self._lego_color_to_id:
            return self._lego_color_to_id[brickowl_colorname]
        if brickowl_colorname in self._peeron_color_to_id:
            return self._peeron_color_to_id[brickowl_colorname]
        if brickowl_colorname in self._color_name_to_id:
            return self._color_name_to_id[brickowl_colorname]
        if brickowl_colorname.find('transparent') == 0:
            return self.get_colorid_from_brickowl_name(brickowl_colorname.replace('transparent ', 'trans-'))
        if brickowl_colorname.find('gray') != -1:
            return self.get_colorid_from_brickowl_name(brickowl_colorname.replace('gray', 'grey'))

        print("!!! Name:", brickowl_colorname, "is unmatched")
        return None
