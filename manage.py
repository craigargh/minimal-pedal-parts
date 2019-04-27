import argparse

from pedalparts.actions import add_pedal, list_missing_parts, add_part, add_parts


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


if __name__ == '__main__':
    main()
