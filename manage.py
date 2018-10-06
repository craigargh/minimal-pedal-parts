import argparse

from pedalparts import parttools, pedaltools


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['add_pedal', 'add_part', 'missing'])

    parser.add_argument('--pedals', required=False, nargs='*')

    parser.add_argument('--category', required=False)
    parser.add_argument('--value', required=False)
    parser.add_argument('--qty', required=False, type=int)

    args = parser.parse_args()

    if args.mode == 'add_pedal':
        add_pedal()

    elif args.mode == 'missing':
        list_missing_parts(args.pedals)

    elif args.mode == 'add_part':
        add_part(args.category, args.value, args.qty)


def add_pedal():
    # TODO: test

    name = input('Enter the pedal name: ')
    print('Enter the parts (press enter twice to finish):')

    parts = []

    raw_part = input('')

    while raw_part != '':
        new_part = parttools.parse(raw_part)
        parts.append(new_part)

        raw_part = input('')

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

    for item in missing:
        output = f"{item['value']} {item['category']} (qty: {item['qty']})"
        print(output)


def add_part(category, value, qty):
    part = {
        'category': category,
        'value': value,
        'qty': qty,
    }

    parttools.save(part)


if __name__ == '__main__':
    main()
