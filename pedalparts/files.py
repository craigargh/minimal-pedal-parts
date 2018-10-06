import json


def save(path, data):
    with open(path, 'w+') as open_file:
        json.dump(data, open_file, indent=2)


def load(path):
    try:
        with open(path, 'r') as open_file:
            data = json.load(open_file)

    except FileNotFoundError:
        data = []

    return data
