import unittest
import rebrickable_colors

OPEN_TABLE_TAG = "<html><header></header><body><table class='table'>"
HEADER = """<tr class='row_header'>
                    <td></td>
                    <td>ID</td>
                    <td>Name</td>
                    <td>RGB</td>
                    <td>Num Parts</td>
                    <td>Num Sets</td>
                    <td>From Year</td>
                    <td>To Year</td>
                    <td>LEGO Color</td>
                    <td>LDraw Color</td>
                    <td>BrickLink Color</td>
                    <td>Peeron Color</td>
            </tr>
"""
COLOR_ROW1 = "<tr><td><img src='/img/pieces/75/3003.png' height='50px'></td><td>75</td><td>Speckle Black-Copper</td><td>#000000</td><td>7</td><td>3</td><td>2006</td><td>2006</td><td></td><td>{75}</td><td>{116}</td><td>{BlackCopperGlitter}</td></tr>"
COLOR_ROW2_TRANS_BLACK = "<tr><td><img src='/img/pieces/32/3003.png' height='50px'></td><td>32</td><td>Trans-Black IR Lens</td><td style='background-color: 635F52;'>#635F52</td><td>0</td><td>0</td><td></td><td></td><td></td><td>{32}</td><td></td><td></td></tr>"
COLOR_ROW3_CHROME_SILVER = "<tr><td><img src='/img/pieces/383/3003.png' height='50px'></td><td>383</td><td>Chrome Silver</td><td>#E0E0E0</td><td>2363</td><td>428</td><td>1977</td><td>2014</td><td>{\"Metalized Silver\"}</td><td>{383}</td><td>{22}</td><td>{ChromeSilver}</td></tr>"
COLOR_ROW4_WHITE = "<tr><td><img src='/img/pieces/15/3003.png' height='50px'></td><td>15</td><td>White</td><td>#FFFFFF</td><td>248682</td><td>6225</td><td>1950</td><td>2014</td><td>{White}</td><td>{15}</td><td>{1}</td><td>{White}</td></tr>"
COLOR_ROW5_BROWN = "<tr><td><img src='/img/pieces/6/3003.png' height='50px'></td><td>6</td><td>Brown</td><td>#583927</td><td>9037</td><td>905</td><td>1974</td><td>2014</td><td>{\"Earth Orange\",Brown}</td><td>{6}</td><td>{8}</td><td>{OldBrown}</td></tr>"
CLOSE_TABLE_TAG = "</table></body></html>"
WHOLE_TABLE = OPEN_TABLE_TAG + HEADER + "%s" + CLOSE_TABLE_TAG

class ColorTableParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = rebrickable_colors.ColorTableParser()

    def test_no_rows_except_header(self):
        """
        Make sure no rows works fine too
        """
        self.parser.feed(WHOLE_TABLE % "")
        self.assertEqual(self.parser.table_data, [])

    def test_color_row1(self):
        """
        Simple test of the first row of actual data
        """
        self.parser.feed(WHOLE_TABLE % COLOR_ROW1)
        self.assertEqual(self.parser.table_data, [{'Name': 'Speckle Black-Copper', 'Num Sets': 3, 'Peeron Color': ['BlackCopperGlitter'], 'Num Parts': 7, 'RGB': '#000000', 'BrickLink Color': [116], 'From Year': 2006, 'LDraw Color': [75], 'ID': 75, 'To Year': 2006}])

    def test_color_row2_trans_black(self):
        """
        Test a row with very few fields filled in
        """
        self.parser.feed(WHOLE_TABLE % COLOR_ROW2_TRANS_BLACK)
        self.assertEqual(self.parser.table_data, [{'Name': 'Trans-Black IR Lens', 'Num Sets': 0, 'Num Parts': 0, 'RGB': '#635F52', 'LDraw Color': [32], 'ID': 32}])

    def test_color_row3_chrome_silver(self):
        """
        Make sure single color in the LEGO Color column works and no quotes retained within string.
        """
        self.parser.feed(WHOLE_TABLE % COLOR_ROW3_CHROME_SILVER)
        self.assertEqual(self.parser.table_data, [{'Name': 'Chrome Silver', 'Num Sets': 428, 'Peeron Color': ['ChromeSilver'], 'Num Parts': 2363, 'RGB': '#E0E0E0', 'LEGO Color': ['Metalized Silver'], 'BrickLink Color': [22], 'From Year': 1977, 'LDraw Color': [383], 'ID': 383, 'To Year': 2014}])

    def test_color_row4_white(self):
        """
        Make sure single color in the LEGO Color column works when there are no quotes in original string
        """
        self.parser.feed(WHOLE_TABLE % COLOR_ROW4_WHITE)
        self.assertEqual(self.parser.table_data, [{'Name': 'White', 'Num Sets': 6225, 'Peeron Color': ['White'], 'Num Parts': 248682, 'RGB': '#FFFFFF', 'LEGO Color': ['White'], 'BrickLink Color': [1], 'From Year': 1950, 'LDraw Color': [15], 'ID': 15, 'To Year': 2014}])

    def test_color_row5_brown(self):
        """
        Make sure array of LEGO Colors works
        """
        self.parser.feed(WHOLE_TABLE % COLOR_ROW5_BROWN)
        self.assertEqual(self.parser.table_data, [{'Name': 'Brown', 'Num Sets': 905, 'Peeron Color': ['OldBrown'], 'Num Parts': 9037, 'RGB': '#583927', 'LEGO Color': ['Earth Orange', 'Brown'], 'BrickLink Color': [8], 'From Year': 1974, 'LDraw Color': [6], 'ID': 6, 'To Year': 2014}])


class ColorTableTest(unittest.TestCase):

    def setUp(self):
        # Setup
        self.data = [{'Name': 'Speckle Black-Copper', 'Num Sets': 3, 'Peeron Color': ['BlackCopperGlitter', 'BlackGlitter'], 'Num Parts': 7, 'RGB': '#000000', 'BrickLink Color': [116], 'From Year': 2006, 'LDraw Color': [75], 'ID': 75, 'To Year': 2006},
                {'Name': 'Chrome Silver', 'Num Sets': 429, 'Peeron Color': ['ChromeSilver'], 'Num Parts': 2364, 'RGB': '#E0E0E0', 'LEGO Color': ['Metalized Silver'], 'BrickLink Color': [22], 'From Year': 1977, 'LDraw Color': [383], 'ID': 383, 'To Year': 2014},
                {'ID': 999},
                {'ID': 666, 'LEGO Color': ['Trans-Green']},
                {'ID': 555, 'LEGO Color': ['medium grey']}]

        # Call method-under-test
        self.instance = rebrickable_colors.ColorTable(self.data)

    def test__parse(self):
        instance = self.instance

        # Verification
        self.assertEqual(instance._data, self.data)

        self.assertEqual(len(instance._lego_color_to_id), 3)
        self.assertEqual(instance._lego_color_to_id['metalized silver'], 383)
        self.assertEqual(instance._lego_color_to_id['trans-green'], 666)
        self.assertEqual(instance._lego_color_to_id['medium grey'], 555)

        self.assertEqual(len(instance._peeron_color_to_id), 3)
        self.assertEqual(instance._peeron_color_to_id['blackcopperglitter'], 75)
        self.assertEqual(instance._peeron_color_to_id['blackglitter'], 75)
        self.assertEqual(instance._peeron_color_to_id['chromesilver'], 383)

        self.assertEqual(len(instance._color_name_to_id), 2)
        self.assertEqual(instance._color_name_to_id['speckle black-copper'], 75)
        self.assertEqual(instance._color_name_to_id['chrome silver'], 383)

    def test_get_color_id_from_brick_owl_name(self):
        self.assertEqual(self.instance.get_colorid_from_brickowl_name('Metalized Silver'), 383)
        self.assertEqual(self.instance.get_colorid_from_brickowl_name('blackglitter'), 75)
        self.assertEqual(self.instance.get_colorid_from_brickowl_name('speckle black-copper'), 75)
        self.assertEqual(self.instance.get_colorid_from_brickowl_name('transparent green'), 666)
        self.assertEqual(self.instance.get_colorid_from_brickowl_name('medium gray'), 555)
        self.assertEqual(self.instance.get_colorid_from_brickowl_name('blather'), None)
        self.assertEqual(self.instance.get_colorid_from_brickowl_name('transparent blather'), None)
        self.assertEqual(self.instance.get_colorid_from_brickowl_name('blather gray'), None)