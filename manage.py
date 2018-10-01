import argparse

from pedalparts import part, pedal


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode')

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
        new_part = part.parse(raw_part)
        parts.append(new_part)

        raw_part = input('')

    new_pedal = pedal.create(name, parts)

    pedal.save(new_pedal)

    print(f'Saved {name}')


if __name__ == '__main__':
    main()
