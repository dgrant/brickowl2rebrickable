
import csv
import urllib.request
import urllib.parse
import json

from rebrickable_colors import get_color_conversion_table

def do_http_get(url, params=None):
    """
    Perform an http get, returning the response data.

    :param url: full url including protocol and port
    :param params: dictionary of parameters
    :return: the body of the HTTP response
    """
    if params != None:
        url = (url + '?%s') % urllib.parse.urlencode(params)
    f = urllib.request.urlopen(url)
    return f.read().decode('utf8')

class BrickOwl(object):

    URL = 'https://api.brickowl.com/v1/order/items'

    def __init__(self, api_key):
        self._api_key = api_key

    def fetch_order(self, order_id):
        params = {'key': self._api_key, 'order_id': order_id}
        return do_http_get(self.URL, params)

    def export_to_rebrickable_csv(self, order_id):
        color_table = get_color_conversion_table()
        brick_owl_order_json = json.loads(self.fetch_order(order_id))
        print(brick_owl_order_json)

        # Fix up colors
        for item in brick_owl_order_json:
            print("****", item['name'])
            color_name = item['color_name']
            if color_name == "":
                print("!!! Skipping item", item['name'], "because it has no color")
                continue
            item['rebrickable_color_id'] = color_table.get_color_id_from_brick_owl_name(color_name)
            #print("color name", color_name, "=> rebrickable color id=", rebrickable_color_id)

        # Create a line for Rebrickable CSV file
        rows = []
        for item in brick_owl_order_json:
            print(item)
            done = False
            # TODO: need to change this to be smarter, to choose ldraw or design_id or peeron_id, depending on which one has more sets in Rebrickable
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
            rows.append([part_id, item['rebrickable_color_id'], item['ordered_quantity']])

        # Writes lines to CSV file in Rebrickable format
        with open('brick_owl_order_{0}.csv'.format(order_id), 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Part', 'Color', 'Num'])
            for row in rows:
                writer.writerow(row)


    def export_to_rebrickable_csvs(self, order_ids):
        for order_id in order_ids:
            self.export_to_rebrickable_csv(order_id)
