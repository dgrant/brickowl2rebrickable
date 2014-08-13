#!/usr/bin/env python3
import argparse
import collections
import low_level


def combine(list_of_list_of_parts):
    result = collections.OrderedDict()
    for list_of_parts in list_of_list_of_parts:
        for row in list_of_parts:
            (part_no, color, quantity) = row
            key = (part_no, color)
            quantity = int(quantity)
            if key not in result:
                result[key] = 0
            result[key] += quantity

    combined_rows = []
    for key, quantity in result.items():
        (part_no, color_id) = key
        combined_rows.append([part_no, color_id, str(quantity)])
    return combined_rows


def combine_rebrickable_csv(csv_files, output_file):
    list_of_list_of_parts = []
    for file in csv_files:
        rows = low_level.read_csv_file(file)
        if rows[0] != ['Part', 'Color', 'Num']:
            raise Exception('File {0} does not look like a Rebrickable csv file'.format(file))
        list_of_list_of_parts.append(rows[1:])
    combined_parts = combine(list_of_list_of_parts)
    low_level.write_csv_file(output_file, combined_parts, header=['Part', 'Color', 'Num'])


def main():
    parser = argparse.ArgumentParser(description='Combine multiple Rebrickable csv files into one')
    parser.add_argument('csv_files', metavar='ORDER_NUM', nargs='+', help='Rebrickable csv file names')
    args = parser.parse_args()

    combine_rebrickable_csv(args.csv_files, 'combined.csv')


if __name__ == '__main__':
    main()
