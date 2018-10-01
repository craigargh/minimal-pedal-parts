from pedalparts import part, pedal


def create_pedal():
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
