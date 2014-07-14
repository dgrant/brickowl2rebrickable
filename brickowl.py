
import os
import json
import low_level
import rebrickable

class BrickOwl(object):

    URL = 'https://api.brickowl.com/v1/order/items'

    def __init__(self, api_key):
        self._api_key = api_key
        self.rebrickable = rebrickable.Rebrickable()

    def fetch_order(self, order_id):
        params = {'key': self._api_key, 'order_id': order_id}
        return low_level.do_http_get(self.URL, params)

    def export_to_rebrickable_csv(self, order_id, output_dir):
        order_json = self.fetch_order(order_id)
        brick_owl_order_json = json.loads(order_json)

        # Fix up colors
        for item in brick_owl_order_json:
            color_name = item['color_name']
            if color_name == "":
                print('!!! Skipping item "{0}" because it has no color'.format(item['name']))
                continue
            item['rebrickable_color_id'] = self.rebrickable.get_color_id_from_brick_owl_name(color_name)

        # Create a line for Rebrickable CSV file
        rows = []
        for item in brick_owl_order_json:
            #print(item)
            done = False
            # TODO: need to change this to be smarter, to choose ldraw or design_id or peeron_id, depending on which one has more sets in Rebrickable
            #for id_type in ('ldraw', 'design_id',):
            for id_type in ('design_id', 'ldraw',):
                #print("Trying id_type", id_type)
                if not done:
                    for id in item['ids']:
                        #print('id=', id)
                        if id['type'] == id_type:
                            part_id = id['id']
                            #print('part_id=', part_id)
                            done = True
                            break
                if done:
                    break
            else:
                print('!!! Could not find design_id or ldraw id for item: "{0}"'.format(item['name']))
                continue
            rows.append([part_id, item['rebrickable_color_id'], item['ordered_quantity']])

        low_level.write_csv_file(os.path.join(output_dir, 'brick_owl_order_{0}.csv'.format(order_id)), rows, ['Part', 'Color', 'Num'])


    def export_to_rebrickable_csvs(self, order_ids, output_dir):
        for order_id in order_ids:
            self.export_to_rebrickable_csv(order_id, output_dir)
