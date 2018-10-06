from unittest import TestCase
from unittest.mock import patch

from pedalparts import parttools


class TestParsePart(TestCase):
    def test_part_with_quantity_is_parsed(self):
        result = parttools.parse('resistor, 10k, 3')

        expected = {
            'category': 'resistor',
            'value': '10k',
            'qty': 3
        }

        self.assertEqual(expected, result)

    def test_quantity_defaults_to_1(self):
        result = parttools.parse('resistor, 10k')

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

        result = parttools.add_part([], new_part)

        self.assertEqual([new_part], result)

    def test_part_can_be_added_to_existing_list(self):
        existing_parts = [
            {'category': 'resistor', 'value': '240k', 'qty': 1}
        ]
        new_part = {'category': 'resistor', 'value': '10k', 'qty': 1}

        result = parttools.add_part(existing_parts, new_part)

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

        result = parttools.add_part(existing_parts, new_part)

        expected = [
            {'category': 'resistor', 'value': '10k', 'qty': 2},
        ]

        self.assertEqual(expected, result)


class TestLoadAndSave(TestCase):
    def setUp(self):
        self.files_mock = patch('pedalparts.parttools.files').start()

        self.addCleanup(patch.stopall)

    def test_load_all_open_file(self):
        parttools.load_all()

        self.files_mock.load.assert_called_once_with('parts.json')

    def test_load_all_returns_loaded_data(self):
        self.files_mock.load.return_value = [
            {'category': 'resistor', 'value': '10k', 'qty': 5}
        ]

        result = parttools.load_all()

        expected = [{'category': 'resistor', 'value': '10k', 'qty': 5}]

        self.assertEqual(expected, result)

    def test_save_loads_all_parts(self):
        parttools.save([{'qty': 5}])

        self.files_mock.load.assert_called_once_with('parts.json')

    def test_save_append_new_part_to_existing_parts(self):
        self.files_mock.load.return_value = [
            {'category': 'resistor', 'value': '10k', 'qty': 5}
        ]

        parttools.save(
            {'category': 'resistor', 'value': '100k', 'qty': 5}
        )

        expected = [
            {'category': 'resistor', 'value': '10k', 'qty': 5},
            {'category': 'resistor', 'value': '100k', 'qty': 5}
        ]

        self.files_mock.save.assert_called_once_with('parts.json', expected)

    def test_duplicate_parts_added_to_existing_parts(self):
        self.files_mock.load.return_value = [
            {'category': 'resistor', 'value': '10k', 'qty': 5}
        ]

        parttools.save(
            {'category': 'resistor', 'value': '10k', 'qty': 5}
        )

        expected = [
            {'category': 'resistor', 'value': '10k', 'qty': 10},
        ]

        self.files_mock.save.assert_called_once_with('parts.json', expected)
