from unittest import TestCase

from pedalparts import pedal


class TestCreatePedal(TestCase):
    def test_pedal_name_is_set(self):
        result = pedal.create('Red Baron', [])

        self.assertEqual('Red Baron', result['name'])

    def test_parts_list_is_set(self):
        parts = [
            {'category': 'resistor', 'value': '10k', 'qty': 3},
            {'category': 'resistor', 'value': '100', 'qty': 1},
            {'category': 'capacitor', 'value': '120n', 'qty': 6},
        ]

        result = pedal.create('Red Baron', parts)

        self.assertEqual(parts, result['parts'])
