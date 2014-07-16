import html.parser

__author__ = 'david'


def strarray(data):
    data = data.strip('{}')
    data = data.split(',')
    data = [x.strip('"') for x in data]
    return data


def intarray(data):
    return [int(x) for x in strarray(data)]


class ColorTableParser(html.parser.HTMLParser):
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
        self._in_table = False
        self._in_row = False
        self._in_col = False
        self._row = 0
        self._col = 0
        self._in_header = False
        self._header_data = {}
        self._row_data = None
        self.table_data = []

    def handle_starttag(self, tag, attrs):
        if not self._in_table and tag.lower() == 'table' and ('class', 'table') in attrs:
            self._in_table = True
        elif self._in_table:
            if not self._in_row and tag.lower() == 'tr':
                self._in_row = True
                self._row_data = {}
            elif self._in_row and not self._in_col and tag.lower() == 'td':
                self._in_col = True

    def handle_endtag(self, tag):
        if tag.lower() == 'table':
            self._in_table = False
        elif tag.lower() == 'td':
            self._in_col = False
            self._col += 1
        elif tag.lower() == 'tr':
            self._in_row = False
            self._row += 1
            self._col = 0
            if not self._in_header:
                self.table_data.append(self._row_data)
            else:
                self._in_header = False
            self._row_data = None

    def handle_data(self, data):
        if self._in_row and self._in_col:
                if data == 'ID':
                self._in_header = True
                self._row -= 1

            if self._in_header:
                self._header_data[self._col] = data
            else:
                header_name = self._header_data[self._col]
                self._row_data[header_name] = self.TYPES[header_name](data)


class ColorTable(object):
    def __init__(self, data):
        self._data = data
        self._lego_color_to_id = {}
        self._peeron_color_to_id = {}
        self._color_name_to_id = {}
        self._parse()

    def _parse(self):
        for color in self._data:
            if 'LEGO Color' in color:
                for lego_color_name in color['LEGO Color']:
                    self._lego_color_to_id[lego_color_name.lower()] = color['ID']
            if 'Peeron Color' in color:
                for peeron_color_name in color['Peeron Color']:
                    self._peeron_color_to_id[peeron_color_name.lower()] = color['ID']
            if 'Name' in color:
                self._color_name_to_id[color['Name'].lower()] = color['ID']

    def get_colorid_from_brickowl_name(self, name):
        name = name.lower()
        if name in self._lego_color_to_id:
            return self._lego_color_to_id[name]
        if name in self._peeron_color_to_id:
            return self._peeron_color_to_id[name]
        if name in self._color_name_to_id:
            return self._color_name_to_id[name]
        if name.find('transparent') == 0:
            return self.get_colorid_from_brickowl_name(name.replace('transparent ', 'trans-'))
        if name.find('gray') != -1:
            return self.get_colorid_from_brickowl_name(name.replace('gray', 'grey'))

        print("!!! Name:", name, "is unmatched")
        return None
