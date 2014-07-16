"""
BrickOwl API class
"""
import os
import json

import low_level
import rebrickable


class BrickOwl(object):
    """
    BrickOwl API.
    """

    URL = 'https://api.brickowl.com/v1/order/items'

    def __init__(self, brickowl_api_key, rebrickable_api_Key):
        self._api_key = brickowl_api_key
        self.rebrickable = rebrickable.Rebrickable(rebrickable_api_Key)

    def fetch_order(self, order_id):
        """
        Fetch an order from BrickOwl.

        :param order_id: BrickOwl order id
        :return: order result as a dictionary
        """
        params = {'key': self._api_key, 'order_id': order_id}
        ret_json = low_level.do_http_get(self.URL, params)
        ret_dict = json.loads(ret_json)
        return ret_dict

    def export_to_rebrickable_csv(self, order_id, output_dir):
        """
        Export a BrickOwl order to a Rebrickable CSV file.

        :param order_id: BrickOwl order id
        :param output_dir: the directory where the .csv file should be saved
        :return: nothing
        """
        brick_owl_order_json = self.fetch_order(order_id)

        # Fix up colors
        for item in brick_owl_order_json:
            color_name = item['color_name']
            if color_name == '':
                continue
            item['rebrickable_color_id'] = self.rebrickable.get_colorid_from_brickowl_name(color_name)

        # Create a line for Rebrickable CSV file
        rows = []
        for item in brick_owl_order_json:
            if 'rebrickable_color_id' not in item:
                print('!!! Skipping item "{0}" because it has no color'.format(item['name']))
                continue
            # print(item)
            ids = []
            design_id = None
            for _id in item['ids']:
                # Check that the type is one of the valid ones for searching in rebrickable
                if _id['type'] not in ['ldraw', 'design_id', 'peeron_id']:
                    continue
                # Record the design_id. design_id is used as a backup, just in case none of the other part numbers
                # are good. design_id will be OK.
                if _id['type'] == 'design_id':
                    design_id = _id['id']
                the_id = _id['id']
                if the_id not in ids:
                    ids.append(the_id)
            best_id = self.rebrickable.get_best_part_match(ids)
            # Just in case none of them can be found on rebrickable, use the design_id
            if best_id is None:
                best_id = design_id
            rows.append([best_id, item['rebrickable_color_id'], item['ordered_quantity']])

        low_level.write_csv_file(os.path.join(output_dir, 'brick_owl_order_{0}.csv'.format(order_id)),
                                 rows, ['Part', 'Color', 'Num'])

    def export_to_rebrickable_csvs(self, order_ids, output_dir):
        """
        Export BrickOwl orders to a Rebrickable CSV files.

        :param order_ids: a list of BrickOwl order ids
        :param output_dir: the directory where the .csv files should be saved
        :return: nothing
        """
        for order_id in order_ids:
            self.export_to_rebrickable_csv(order_id, output_dir)
