import unittest
from mock import Mock, MagicMock, patch, call

import low_level
import brickowl

class TestBrickOwl(unittest.TestCase):

    @patch('low_level.do_http_get')
    def test_fetch_order(self, do_http_get_mock):
        # Setup
        json = "['some json here']"
        brickOwl = brickowl.BrickOwl("API_KEY")
        do_http_get_mock.return_value = json

        # Call method-under-test
        ret = brickOwl.fetch_order(1)

        # Verification
        low_level.do_http_get.assert_called_once_with("https://api.brickowl.com/v1/order/items", {'order_id': 1, 'key': 'API_KEY'})
        self.assertEqual(ret, json)

    @patch('low_level.write_csv_file')
    @patch('rebrickable.Rebrickable')
    @patch('brickowl.BrickOwl.fetch_order')
    def test_export_to_rebrickable_csv(self, fetch_order_mock, RebrickableMock, write_csv_file_mock):
        # Setup
        color_mapping = {'Dark Stone Gray': '72', 'White': '15'}
        order_id = '1234'
        brickOwl = brickowl.BrickOwl("API_KEY")
        fetch_order_mock.return_value ='[{"image_small":"\/\/img.brickowl.com\/files\/image_cache\/small\/lego-dark-stone-gray-tile-1-x-2-grille-with-bottom-groove-2412-30-363948-50.png","condition":"New","name":"LEGO Dark Stone Gray Tile 1 x 2 Grille (with Bottom Groove) (2412)","boid":"363948-50","weight":"0.230","public_note":"","ordered_quantity":"10","order_item_id":"608615","base_price":"0.098","color_name":"Dark Stone Gray","color_id":"50","lot_id":"284854","ids":[{"id":"2412","type":"design_id"},{"id":"2412b","type":"ldraw"},{"id":"2412b","type":"peeron_id"},{"id":"363948-50","type":"boid"},{"id":"4210631","type":"item_no"},{"id":"4210631","type":"item_no"}]},{"image_small":"\/\/img.brickowl.com\/files\/image_cache\/small\/lego-white-plate-1-x-2-with-horizontal-clip-on-end-63868-30-537281-92.png","condition":"New","name":"LEGO White Plate 1 x 2 with Horizontal Clip on End (63868)","boid":"537281-92","weight":"0.460","public_note":"","ordered_quantity":"4","order_item_id":"608617","base_price":"0.082","color_name":"White","color_id":"92","lot_id":"287690","ids":[{"id":"4535737","type":"item_no"},{"id":"4535737","type":"item_no"},{"id":"537281-92","type":"boid"},{"id":"63868","type":"design_id"},{"id":"63868","type":"design_id"},{"id":"63868","type":"ldraw"},{"id":"63868","type":"peeron_id"}]},{"image_small":"\/\/img.brickowl.com\/files\/image_cache\/small\/lego-unnamed-city-minifigure-83656-1.png","condition":"New","name":"LEGO Unnamed City Minifigure","boid":"83656","weight":10,"public_note":"","ordered_quantity":"1","order_item_id":"574979","base_price":"1.620","color_name":"","color_id":0,"lot_id":null,"ids":[{"id":"83656","type":"boid"},{"id":"nfi.tow.hos.2012.06","type":"mf_tax"}]}]'
        RebrickableMock.return_value.get_color_id_from_brick_owl_name.side_effect = lambda x: color_mapping[x]

        # Call method-under-test
        brickOwl.export_to_rebrickable_csv(order_id, output_dir='.')

        # Verification
        fetch_order_mock.assert_called_once_with(order_id)
        expected_rows = [['2412', '72', '10'], ['63868', '15', '4']]
        write_csv_file_mock.assert_called_once_with('./brick_owl_order_{0}.csv'.format(order_id), expected_rows,
                                                    ['Part', 'Color', 'Num'])

    def test_export_to_rebrickable_csvs(self):
        # Setup
        b = brickowl.BrickOwl("API_KEY")
        b.export_to_rebrickable_csv = Mock()

        # Call method-under-test
        b.export_to_rebrickable_csvs(['1', '2'], output_dir='.')

        # Verification
        self.assertEqual(b.export_to_rebrickable_csv.mock_calls, [call('1', '.'), call('2', '.')])

