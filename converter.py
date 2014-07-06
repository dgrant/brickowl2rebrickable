
import csv
import urllib.request
import urllib.parse
import json

from rebrickable_colors import get_color_conversion_table

class BrickOwl(object):

    URL = 'https://api.brickowl.com/v1/order/items?%s'

    def __init__(self, api_key):
        self._api_key = api_key

    def fetch_order(self, order_id):
        params = urllib.parse.urlencode({'key': self._api_key, 'order_id': order_id})
        f = urllib.request.urlopen(self.URL % params)
        return f.read().decode('utf8')

    def create_rebrickable_csv(self, brick_owl_order_number):
        color_table = get_color_conversion_table()
        brick_owl_order_json = json.loads(self.fetch_order(brick_owl_order_number))
        print(brick_owl_order_json)
        for item in brick_owl_order_json:
            print("****", item['name'])
            color_name = item['color_name']
            if color_name == "":
                print("!!! Skipping item", item['name'], "because it has no color")
                continue
            item['rebrickable_color_id'] = color_table.get_color_id_from_brick_owl_name(color_name)
            #print("color name", color_name, "=> rebrickable color id=", rebrickable_color_id)

        with open('brick_owl_order_{0}.csv'.format(brick_owl_order_number), 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Part', 'Color', 'Num'])
            for item in brick_owl_order_json:
                print(item)
                done = False
                #for id_type in ('ldraw', 'design_id',):
                for id_type in ('design_id', 'ldraw',):
                    print("Trying id_type", id_type)
                    if not done:
                        for id in item['ids']:
                            print('id=', id)
                            if id['type'] == id_type:
                                part_id = id['id']
                                print('part_id=', part_id)
                                done = True
                                break
                    if done:
                        break
                else:
                    print("!!! Could not find design_id or ldraw id for item: ", item['name'])
                    continue
                writer.writerow([part_id, item['rebrickable_color_id'], item['ordered_quantity']])


    def create_rebrickable_csvs(self, order_ids):
        for order_id in order_ids:
            self.create_rebrickable_csv(order_id)
