import copy


def parse(raw_part):
    # TODO: Lowercase category

    split = raw_part.split(', ')

    try:
        qty = int(split[2])
    except IndexError:
        qty = 1

    return {
        'category': split[0],
        'value': split[1],
        'qty': qty,
    }


def add_part(parts_list, part):
    parts = copy.deepcopy(parts_list)

    if part_exists(parts_list, part):
        parts = update_qty(parts_list, part)

    else:
        parts.append(part)

    return parts


def part_exists(parts_list, new_part):
    duplicates = [
        part
        for part in parts_list
        if is_same(part, new_part)
    ]

    return len(duplicates) > 0


def update_qty(parts_list, new_part):
    parts = copy.deepcopy(parts_list)

    for part in parts:
        if is_same(part, new_part):
            old_qty = part['qty']
            add_qty = new_part['qty']

            part['qty'] = old_qty + add_qty

    return parts


def is_same(part_1, part_2):
    return part_1['category'] == part_2['category'] and part_1['value'] == part_2['value']


def save(parts_list):
    pass


def load_all():
    return []
