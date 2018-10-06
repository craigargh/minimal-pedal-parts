import json

from pedalparts import parttools


def create(name, parts) -> dict:
    return {
        'name': name,
        'parts': parts,
    }


def save(pedal):
    # TODO: Check for duplicate pedal names

    pedals = load_all()
    pedals.append(pedal)

    with open('pedals.json', 'w+') as pedals_file:
        json.dump(pedals, pedals_file, indent=2)


def load_all() -> list:
    """ loads pedals from json file """
    try:
        with open('pedals.json', 'r') as pedals_file:
            pedals = json.load(pedals_file)

    except FileNotFoundError:
        pedals = []

    return pedals


def list_missing_parts(pedals, parts) -> list:
    all_pedal_parts = combine_all_pedal_parts(pedals)

    missing = []

    for pedal_part in all_pedal_parts:
        found = False

        for part in parts:
            if parttools.is_same(pedal_part, part):
                found = True

                missing_part = check_qty(part, pedal_part)
                if missing_part:
                    missing.append(missing_part)

        if not found:
            missing.append(pedal_part)

    return missing


def combine_all_pedal_parts(pedals):
    parts = []

    for pedal in pedals:
        for part in pedal['parts']:
            parts = parttools.add_part(parts, part)

    return parts


def check_qty(part, pedal_part):
    qty_diff = pedal_part['qty'] - part['qty']

    if qty_diff <= 0:
        return {}

    return {
        'category': part['category'],
        'value': part['value'],
        'qty': qty_diff,
    }
