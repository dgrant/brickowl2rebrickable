#!/usr/bin/env python3
"""
Script to convert BrickOwl orders numbers into CSV files that can be imported into Rebrickable.
"""

import argparse

import brickowl
import brickowl2rebrickable_conf

DEFAULT_OUTPUTDIR = '.'


def brickowl2rebrickable(brickowl_api_key, rebrickable_api_key, brickowl_orders, output_dir=DEFAULT_OUTPUTDIR):
    """
    Given a list of BrickOwl order ids, convert the order information into a list of parts in Rebrickable format
    in a CSV file.

    :param brickowl_api_key: BrickOwl.com API key
    :param rebrickable_api_key: Rebrickable.com API key
    :param brickowl_orders: a list of BrickOwl order IDs
    :param output_dir: a directory where the Rebrickable CSV files should be saved.
    :return: nothing
    """
    if brickowl_api_key is None:
        brickowl_api_key = brickowl2rebrickable_conf.get_brickowl_api_key()
        if brickowl_api_key is None:
            raise Exception("No BrickOwl API key in {0} or on command line".format(
                brickowl2rebrickable_conf.CONF_FILE_NAME))
    if rebrickable_api_key is None:
        rebrickable_api_key = brickowl2rebrickable_conf.get_rebrickable_api_key()
        if rebrickable_api_key is None:
            raise Exception('No Rebrickable API key in {0} or on command line'.format(
                brickowl2rebrickable_conf.CONF_FILE_NAME))
    brickowl_obj = brickowl.BrickOwl(brickowl_api_key, rebrickable_api_key)
    brickowl_obj.export_to_rebrickable_csvs(brickowl_orders, output_dir=output_dir)


def main():
    """
    Main-entry point. Parse command-line arguments then call brickowl2rebrickable.

    :return: nothing
    """
    parser = argparse.ArgumentParser(description='Convert Brickowl orders into Rebrickable csv files')
    parser.add_argument('-b', '--brickowl_api_key', metavar='BRICKOWL_API_KEY',
                        help='Brickowl API key (overrides value in conf file')
    parser.add_argument('-r', '--rebrickable_api_key', metavar='REBRICKABLE_API_KEY',
                        help='Rebrickable API key (overrides value in conf file')
    parser.add_argument('orders', metavar='ORDER_NUM', nargs='+', help='Brickowl order number(s)')
    args = parser.parse_args()

    brickowl2rebrickable(args.brickowl_api_key, args.rebrickable_api_key, args.orders)

if __name__ == '__main__':
    main()
