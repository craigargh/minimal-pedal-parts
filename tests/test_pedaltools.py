from unittest import TestCase
from unittest.mock import patch

from pedalparts import pedaltools


class TestCreatePedal(TestCase):
    def test_pedal_name_is_set(self):
        result = pedaltools.create('Red Baron', [])

        self.assertEqual('Red Baron', result['name'])

    def test_parts_list_is_set(self):
        parts = [
            {'category': 'resistor', 'value': '10k', 'qty': 3},
            {'category': 'resistor', 'value': '100', 'qty': 1},
            {'category': 'capacitor', 'value': '120n', 'qty': 6},
        ]

        result = pedaltools.create('Red Baron', parts)

        self.assertEqual(parts, result['parts'])


class TestSavePedal(TestCase):
    def setUp(self):
        self.json_load_mock = patch('pedalparts.pedaltools.json.load').start()
        self.open_mock = patch('pedalparts.pedaltools.open').start()
        self.json_save_mock = patch('pedalparts.pedaltools.json.dump').start()

        self.addCleanup(patch.stopall)

    def test_existing_pedals_are_loaded(self):
        new_pedal = {
            'name': 'Hot take',
            'parts': [],
        }

        pedaltools.save(new_pedal)

        open_context_manager = self.open_mock.return_value \
            .__enter__.return_value

        self.json_load_mock.assert_called_once_with(open_context_manager)

    def test_new_pedal_is_added_to_loaded_pedals_and_saved(self):
        self.json_load_mock.return_value = [
            {'name': 'round boy', 'parts': []}
        ]

        new_pedal = {'name': 'Hot take', 'parts': []}
        pedaltools.save(new_pedal)

        open_context_manager = self.open_mock.return_value \
            .__enter__.return_value

        expected = [
            {'name': 'round boy', 'parts': []},
            {'name': 'Hot take', 'parts': []},
        ]

        self.json_save_mock.assert_called_once_with(expected, open_context_manager, indent=2)


class TestMissingParts(TestCase):
    def test_pedal_with_all_parts_in_stock_returns_empty_list(self):
        new_pedal = {
            'parts': [
                {'category': 'capacitor', 'value': '10u', 'qty': 1},
                {'category': 'resistor', 'value': '100k', 'qty': 2},
            ]
        }

        parts = [
            {'category': 'capacitor', 'value': '10u', 'qty': 1},
            {'category': 'resistor', 'value': '100k', 'qty': 2},
        ]

        result = pedaltools.list_missing_parts([new_pedal], parts)

        self.assertEqual([], result)

    def test_pedal_with_missing_parts_lists_parts(self):
        new_pedal = {
            'parts': [
                {'category': 'capacitor', 'value': '10u', 'qty': 1},
                {'category': 'resistor', 'value': '100k', 'qty': 2},
            ]
        }

        parts = [
            {'category': 'capacitor', 'value': '10u', 'qty': 1},
        ]

        result = pedaltools.list_missing_parts([new_pedal], parts)

        expected = [
            {'category': 'resistor', 'value': '100k', 'qty': 2},
        ]

        self.assertEqual(expected, result)

    def test_lower_qty_than_required_is_returned(self):
        new_pedal = {
            'parts': [
                {'category': 'capacitor', 'value': '10u', 'qty': 1},
                {'category': 'resistor', 'value': '100k', 'qty': 2},
            ]
        }

        parts = [
            {'category': 'capacitor', 'value': '10u', 'qty': 1},
            {'category': 'resistor', 'value': '100k', 'qty': 1},
        ]

        result = pedaltools.list_missing_parts([new_pedal], parts)

        expected = [
            {'category': 'resistor', 'value': '100k', 'qty': 1},
        ]

        self.assertEqual(expected, result)

    def test_multiple_pedals_with_in_stock_parts_return_empty_list(self):
        pedals = [
            {
                'parts': [
                    {'category': 'capacitor', 'value': '10u', 'qty': 1},
                    {'category': 'resistor', 'value': '100k', 'qty': 2},
                ]
            },
            {
                'parts': [
                    {'category': 'capacitor', 'value': '120u', 'qty': 1},
                    {'category': 'resistor', 'value': '100k', 'qty': 1},
                ]
            },
        ]

        parts = [
            {'category': 'capacitor', 'value': '10u', 'qty': 1},
            {'category': 'resistor', 'value': '100k', 'qty': 3},
            {'category': 'capacitor', 'value': '120u', 'qty': 1},
        ]

        result = pedaltools.list_missing_parts(pedals, parts)

        self.assertEqual([], result)

    def test_multiple_pedals_with_missing_returns_missing(self):
        pedals = [
            {
                'parts': [
                    {'category': 'capacitor', 'value': '10u', 'qty': 1},
                    {'category': 'resistor', 'value': '100k', 'qty': 2},
                ]
            },
            {
                'parts': [
                    {'category': 'capacitor', 'value': '120u', 'qty': 1},
                    {'category': 'resistor', 'value': '100k', 'qty': 1},
                ]
            },
        ]

        result = pedaltools.list_missing_parts(pedals, [])

        expected = [
            {'category': 'capacitor', 'value': '10u', 'qty': 1},
            {'category': 'resistor', 'value': '100k', 'qty': 3},
            {'category': 'capacitor', 'value': '120u', 'qty': 1},
        ]

        self.assertEqual(expected, result)

    def test_multiple_pedals_with_missing_qty_return_list(self):
        pedals = [
            {
                'parts': [
                    {'category': 'capacitor', 'value': '10u', 'qty': 1},
                    {'category': 'resistor', 'value': '100k', 'qty': 2},
                ]
            },
            {
                'parts': [
                    {'category': 'capacitor', 'value': '120u', 'qty': 1},
                    {'category': 'resistor', 'value': '100k', 'qty': 1},
                ]
            },
        ]

        parts = [
            {'category': 'capacitor', 'value': '10u', 'qty': 1},
            {'category': 'resistor', 'value': '100k', 'qty': 1},
            {'category': 'capacitor', 'value': '120u', 'qty': 1},
        ]

        result = pedaltools.list_missing_parts(pedals, parts)

        expected = [{'category': 'resistor', 'value': '100k', 'qty': 2}]

        self.assertEqual(expected, result)
