#!/usr/bin/env python3

import argparse
import csv
import urllib.request
import urllib.parse
import json

from rebrickable_colors import get_color_conversion_table

BRICK_OWL_API_KEY = 'f1ce0052456f75e0a8d8caafbe73b6c3bc2ed6df18433c71fd43b1f33bf9340a'
URL = 'https://api.brickowl.com/v1/order/items?%s'

def fetch_order(order_id):
    params = urllib.parse.urlencode({'key': BRICK_OWL_API_KEY, 'order_id': order_id})
    f = urllib.request.urlopen(URL % params)
    return f.read().decode('utf8')

def create_rebrickable_csv(brick_owl_order_number):
    color_table = get_color_conversion_table()
    brick_owl_order_json = json.loads(fetch_order(brick_owl_order_number))
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
            for id in item['ids']:
                if id['type'] == 'design_id':
                    design_id = id['id']
                    break
            else:
                print("!!! Could not find design_id for item: ", item['name'])
                continue
            writer.writerow([design_id, item['rebrickable_color_id'], item['ordered_quantity']])


def create_rebrickable_csvs(order_ids):
    for order_id in order_ids:
        create_rebrickable_csv(order_id)

def main():
    parser = argparse.ArgumentParser(description='Convert Brickowl orders into Rebrickable csv files')
    parser.add_argument('orders', metavar='ORDER_NUM', type=int, nargs='+', help='Brickowl order number(s)')
    args = parser.parse_args()
    create_rebrickable_csvs(args.orders)

if __name__ == '__main__':
    main()