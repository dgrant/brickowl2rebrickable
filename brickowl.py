import os
import json
import sys

import low_level
import rebrickable


class BrickOwl(object):

    URL = 'https://api.brickowl.com/v1/order/items'

    def __init__(self, brickowl_api_key, rebrickable_api_Key):
        self._api_key = brickowl_api_key
        self.rebrickable = rebrickable.Rebrickable(rebrickable_api_Key)

    def fetch_order(self, order_id):
        params = {'key': self._api_key, 'order_id': order_id}
        return low_level.do_http_get(self.URL, params)

    def export_to_rebrickable_csv(self, order_id, output_dir):
        order_json = self.fetch_order(order_id)
        # print(order_json)
        brick_owl_order_json = json.loads(order_json)

        # Fix up colors
        for item in brick_owl_order_json:
            color_name = item['color_name']
            if color_name == '':
                continue
            item['rebrickable_color_id'] = self.rebrickable.get_color_id_from_brick_owl_name(color_name)

        # Create a line for Rebrickable CSV file
        rows = []
        for item in brick_owl_order_json:
            if 'rebrickable_color_id' not in  item:
                print('!!! Skipping item "{0}" because it has no color'.format(item['name']))
                continue
            # print(item)
            done = False
            # TODO: need to change this to be smarter, to choose ldraw or design_id or peeron_id, depending on which
            # one has more sets in Rebrickable
            # for id_type in ('ldraw', 'design_id',):
            ids = []
            design_id = None
            for _id in item['ids']:
                if _id['type'] not in ['ldraw', 'design_id', 'peeron_id']:
                    continue
                if _id['type'] == 'design_id':
                    design_id = _id['id']
                the_id = _id['id']
                if the_id not in ids:
                    ids.append(the_id)
            best_id = self.rebrickable.get_best_part_match(ids)
            # Just in case none of them can be found on rebrickable, use the design_id
            if best_id == None:
                best_id = design_id
            rows.append([best_id, item['rebrickable_color_id'], item['ordered_quantity']])

        low_level.write_csv_file(os.path.join(output_dir, 'brick_owl_order_{0}.csv'.format(order_id)),
                                 rows, ['Part', 'Color', 'Num'])

    def export_to_rebrickable_csvs(self, order_ids, output_dir):
        for order_id in order_ids:
            self.export_to_rebrickable_csv(order_id, output_dir)
