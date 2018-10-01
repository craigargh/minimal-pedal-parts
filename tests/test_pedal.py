from unittest import TestCase
from unittest.mock import patch

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


class TestSavePedal(TestCase):
    def setUp(self):
        self.json_load_mock = patch('pedalparts.pedal.json.load').start()
        self.open_mock = patch('pedalparts.pedal.open').start()
        self.json_save_mock = patch('pedalparts.pedal.json.dump').start()

        self.addCleanup(patch.stopall)

    def test_existing_pedals_are_loaded(self):
        new_pedal = {
            'name': 'Hot take',
            'parts': [],
        }

        pedal.save(new_pedal)

        open_context_manager = self.open_mock.return_value \
            .__enter__.return_value

        self.json_load_mock.assert_called_once_with(open_context_manager)

    def test_new_pedal_is_added_to_loaded_pedals_and_saved(self):
        self.json_load_mock.return_value = [
            {'name': 'round boy', 'parts': []}
        ]

        new_pedal = {'name': 'Hot take', 'parts': []}
        pedal.save(new_pedal)

        open_context_manager = self.open_mock.return_value \
            .__enter__.return_value

        expected = [
            {'name': 'round boy', 'parts': []},
            {'name': 'Hot take', 'parts': []},
        ]

        self.json_save_mock.assert_called_once_with(expected, open_context_manager)
