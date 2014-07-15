#!/usr/bin/env python3

import argparse
import brickowl
import brickowl2rebrickable_conf
import sys

DEFAULT_OUTPUTDIR = '.'

def brickowl2rebrickable(brickowl_api_key, brickowl_orders, output_dir=DEFAULT_OUTPUTDIR):
    if brickowl_api_key is None:
        brickowl_api_key = brickowl2rebrickable_conf.get_brickowl_api_key()
        if brickowl2rebrickable_conf.get_brickowl_api_key() is None:
            raise Exception("No BrickOwl API key in {0} or on command line".format(brickowl2rebrickable_conf.CONF_FILE_NAME))
    b = brickowl.BrickOwl(brickowl_api_key)
    b.export_to_rebrickable_csvs(brickowl_orders, output_dir=output_dir)

def main():
    parser = argparse.ArgumentParser(description='Convert Brickowl orders into Rebrickable csv files')
    parser.add_argument('-b', '--brickowl_api_key', metavar='BRICKOWL_API_KEY',
                        help='Brickowl API key (overrides value in conf file')
    parser.add_argument('orders', metavar='ORDER_NUM', nargs='+', help='Brickowl order number(s)')
    args = parser.parse_args()

    brickowl2rebrickable(args.brickowl_api_key, args.orders)

if __name__ == '__main__':
    main()
