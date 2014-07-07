#!/usr/bin/env python3

import argparse
from converter import BrickOwl

def main():
    parser = argparse.ArgumentParser(description='Convert Brickowl orders into Rebrickable csv files')
    parser.add_argument('api_key', metavar='API_KEY', help='Brickowl API key')
    parser.add_argument('orders', metavar='ORDER_NUM', type=int, nargs='+', help='Brickowl order number(s)')
    args = parser.parse_args()

    b = BrickOwl(args.api_key)
    b.export_to_rebrickable_csvs(args.orders)

if __name__ == '__main__':
    main()
