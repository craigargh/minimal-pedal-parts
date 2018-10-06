import argparse
from itertools import groupby
from operator import itemgetter

from pedalparts import parttools, pedaltools


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['add_pedal', 'add_part', 'add_parts', 'missing'])

    parser.add_argument('--name', required=False)
    parser.add_argument('--file', required=False)

    parser.add_argument('--pedals', required=False, nargs='*')

    parser.add_argument('--category', required=False)
    parser.add_argument('--value', required=False)
    parser.add_argument('--qty', required=False, type=int)

    args = parser.parse_args()

    if args.mode == 'add_pedal':
        add_pedal(args.name, args.file)

    elif args.mode == 'missing':
        list_missing_parts(args.pedals)

    elif args.mode == 'add_part':
        add_part(args.category, args.value, args.qty)

    elif args.mode == 'add_parts':
        add_parts(args.file)


def add_pedal(name, file):
    parts = []

    with open(file, 'r') as parts_file:
        raw_parts = parts_file.readlines()

    for raw_part in raw_parts:
        new_part = parttools.parse(raw_part)
        parts.append(new_part)

    new_pedal = pedaltools.create(name, parts)
    pedaltools.save(new_pedal)

    print(f'Saved {name}')


def list_missing_parts(pedal_names):
    parts = parttools.load_all()
    all_pedals = pedaltools.load_all()

    pedals = [
        pedal
        for pedal in all_pedals
        if pedal['name'] in pedal_names
    ]

    missing = pedaltools.list_missing_parts(pedals, parts)

    missing = sorted(missing, key=itemgetter('category'))
    grouped = groupby(missing, key=itemgetter('category'))

    for group_name, items in grouped:
        print(group_name)

        sorted_items = sorted(items, key=itemgetter('value'))

        for item in sorted_items:
            output = f"{item['value'].ljust(15)}(qty: {item['qty']})"
            print(output)

        print('')


def add_part(category, value, qty):
    part = {
        'category': category,
        'value': value,
        'qty': qty,
    }

    parttools.save(part)

def add_parts(file_name):
    with open(file_name, 'r') as parts_file:
        raw_parts = parts_file.readlines()

    parts = (
        parttools.parse(raw_part)
        for raw_part in raw_parts
    )

    for part in parts:
        parttools.save(part)


if __name__ == '__main__':
    main()
