import argparse

from pedalparts import parttools, pedaltools


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['add_pedal'])

    args = parser.parse_args()

    if args.mode == 'add_pedal':
        add_pedal()


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


if __name__ == '__main__':
    main()
