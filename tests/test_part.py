from unittest import TestCase

from pedalparts import part


class TestParsePart(TestCase):
    def test_part_with_quantity_is_parsed(self):
        result = part.parse('resistor, 10k, 3')

        expected = {
            'category': 'resistor',
            'value': '10k',
            'qty': 3
        }

        self.assertEqual(expected, result)

    def test_quantity_defaults_to_1(self):
        result = part.parse('resistor, 10k')

        expected = {
            'category': 'resistor',
            'value': '10k',
            'qty': 1
        }

        self.assertEqual(expected, result)


class TestAddPartToList(TestCase):
    def test_part_can_be_added_to_empty_list(self):
        new_part = {
            'category': 'resistor',
            'value': '10k',
            'qty': 1,
        }

        result = part.add_part([], new_part)

        self.assertEqual([new_part], result)

    def test_part_can_be_added_to_existing_list(self):
        existing_parts = [
            {'category': 'resistor', 'value': '240k', 'qty': 1}
        ]
        new_part = {'category': 'resistor', 'value': '10k', 'qty': 1}

        result = part.add_part(existing_parts, new_part)

        expected = [
            {'category': 'resistor', 'value': '240k', 'qty': 1},
            {'category': 'resistor', 'value': '10k', 'qty': 1},
        ]

        self.assertEqual(expected, result)

    def test_new_part_qty_is_added_to_existing_qty(self):
        existing_parts = [
            {'category': 'resistor', 'value': '10k', 'qty': 1}
        ]
        new_part = {'category': 'resistor', 'value': '10k', 'qty': 1}

        result = part.add_part(existing_parts, new_part)

        expected = [
            {'category': 'resistor', 'value': '10k', 'qty': 2},
        ]

        self.assertEqual(expected, result)