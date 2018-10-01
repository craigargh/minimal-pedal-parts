import json


def create(name, parts) -> dict:
    return {
        'name': name,
        'parts': parts,
    }


def save(pedal):
    pedals = load_all()
    pedals.append(pedal)

    with open('pedals.json', 'w+') as pedals_file:
        json.dump(pedals, pedals_file)


def load_all() -> list:
    """ loads pedals from json file """
    try:
        with open('pedals.json', 'r') as pedals_file:
            pedals = json.load(pedals_file)

    except FileNotFoundError:
        pedals = []

    return pedals


def list_missing_parts(pedals, parts) -> list:
    return []
