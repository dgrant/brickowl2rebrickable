import json
import unittest
from mock import Mock, MagicMock, patch, call

import low_level
import brickowl

class TestBrickOwl(unittest.TestCase):

    @patch('rebrickable.Rebrickable')
    @patch('low_level.do_http_get')
    def test_fetch_order(self, do_http_get_mock, RebrickableMock):
        # Setup
        json = '[{"name":"foo"}]'
        brickOwl = brickowl.BrickOwl("BRICKOWL_API_KEY", 'REBRICKABLE_API_KEY')
        do_http_get_mock.return_value = json

        # Call method-under-test
        ret = brickOwl.fetch_order(1)

        # Verification
        RebrickableMock.assert_called_once_with('REBRICKABLE_API_KEY')
        low_level.do_http_get.assert_called_once_with("https://api.brickowl.com/v1/order/items", {'order_id': 1, 'key': 'BRICKOWL_API_KEY'})
        self.assertEqual(ret, [{'name': 'foo'}])

    @patch('low_level.write_csv_file')
    @patch('rebrickable.Rebrickable')
    @patch('brickowl.BrickOwl.fetch_order')
    def test_export_to_rebrickable_csv(self, fetch_order_mock, RebrickableMock, write_csv_file_mock):
        # Setup
        color_mapping = {'Dark Stone Gray': '72', 'White': '15'}
        order_id = '1234'
        brick_owl= brickowl.BrickOwl("BRICKOWL_API_KEY", "REBRICKABLE_API_KEY")
        fetch_order_mock.return_value = json.loads("""
        [{"name":"LEGO Dark Stone Gray Tile 1 x 2 Grille (with Bottom Groove) (2412)",
          "ordered_quantity":"10","order_item_id":"608615","base_price":"0.098","color_name":"Dark Stone Gray","color_id":"50","lot_id":"284854",
          "ids":[{"id":"2412","type":"design_id"},{"id":"2412b","type":"ldraw"},{"id":"2412b","type":"peeron_id"},{"id":"363948-50","type":"boid"},{"id":"4210631","type":"item_no"},{"id":"4210631","type":"item_no"}]},
         {"name":"LEGO White Plate 1 x 2 with Horizontal Clip on End (63868)",
          "ordered_quantity":"4","order_item_id":"608617","base_price":"0.082","color_name":"White","color_id":"92","lot_id":"287690",
          "ids":[{"id":"4535737","type":"item_no"},{"id":"4535737","type":"item_no"},{"id":"537281-92","type":"boid"},{"id":"63868","type":"design_id"},{"id":"63868","type":"design_id"},{"id":"63868","type":"ldraw"},{"id":"63868","type":"peeron_id"}]},
         {"name":"Something with no color",
          "ordered_quantity":"4","order_item_id":"608617","base_price":"0.082","color_name":"","color_id":"92","lot_id":"287690",
          "ids":[{"id":"4535737","type":"item_no"},{"id":"4535737","type":"item_no"},{"id":"537281-92","type":"boid"},{"id":"63868","type":"design_id"},{"id":"63868","type":"design_id"},{"id":"63868","type":"ldraw"},{"id":"63868","type":"peeron_id"}]}]
        """)
        r = RebrickableMock.return_value
        r.get_colorid_from_brickowl_name.side_effect = lambda x: color_mapping[x]
        r.get_best_part_match.return_value = 'best_id'

        # Call method-under-test
        brick_owl.export_to_rebrickable_csv(order_id, output_dir='.')

        # Verification
        RebrickableMock.assert_called_once_with('REBRICKABLE_API_KEY')
        fetch_order_mock.assert_called_once_with(order_id)
        expected_rows = [['best_id', '72', '10'], ['best_id', '15', '4']]
        self.assertEqual(r.get_best_part_match.mock_calls, [call(['2412', '2412b']), call(['63868'])])
        write_csv_file_mock.assert_called_once_with('./brick_owl_order_{0}.csv'.format(order_id), expected_rows,
                                                    header=['Part', 'Color', 'Num'])

    @patch('low_level.write_csv_file')
    @patch('rebrickable.Rebrickable')
    @patch('brickowl.BrickOwl.fetch_order')
    def test_export_to_rebrickable_csv_no_partid_found_on_rebrickable(self, fetch_order_mock, RebrickableMock, write_csv_file_mock):
        # Setup
        color_mapping = {'Dark Stone Gray': '72'}
        order_id = '1234'
        brick_owl = brickowl.BrickOwl("BRICKOWL_API_KEY", 'REBRICKABLE_API_KEY')
        fetch_order_mock.return_value = json.loads("""
        [{"name":"LEGO Dark Stone Gray Tile 1 x 2 Grille (with Bottom Groove) (2412)",
          "ordered_quantity":"10","order_item_id":"608615","base_price":"0.098","color_name":"Dark Stone Gray","color_id":"50","lot_id":"284854",
          "ids":[{"id":"2412","type":"design_id"},{"id":"2412b","type":"ldraw"},{"id":"2412b","type":"peeron_id"},{"id":"363948-50","type":"boid"},{"id":"4210631","type":"item_no"},{"id":"4210631","type":"item_no"}]}]
        """)
        r = RebrickableMock.return_value
        r.get_colorid_from_brickowl_name.side_effect = lambda x: color_mapping[x]
        r.get_best_part_match.return_value = None  # make the best part match function return None, ie. no parts found on rebrickable

        # Call method-under-test
        brick_owl.export_to_rebrickable_csv(order_id, output_dir='.')

        # Verification
        RebrickableMock.assert_called_once_with('REBRICKABLE_API_KEY')
        fetch_order_mock.assert_called_once_with(order_id)
        expected_rows = [['2412', '72', '10']]
        self.assertEqual(r.get_best_part_match.mock_calls, [call(['2412', '2412b'])])
        write_csv_file_mock.assert_called_once_with('./brick_owl_order_{0}.csv'.format(order_id), expected_rows,
                                                    header=['Part', 'Color', 'Num'])

    @patch('rebrickable.Rebrickable')
    def test_export_to_rebrickable_csvs(self, RebrickableMock):
        # Setup
        b = brickowl.BrickOwl("BRICKOWL_API_KEY", 'REBRICKABLE_API_KEY')
        b.export_to_rebrickable_csv = Mock()

        # Call method-under-test
        b.export_to_rebrickable_csvs(['1', '2'], output_dir='.')

        # Verification
        RebrickableMock.assert_called_once_with('REBRICKABLE_API_KEY')
        self.assertEqual(b.export_to_rebrickable_csv.mock_calls, [call('1', '.'), call('2', '.')])
