from unittest import TestCase
from unittest.mock import patch, ANY

from pedalparts.files import save, load


class TestSave(TestCase):
    def setUp(self):
        self.open_mock = patch('pedalparts.files.open').start()
        self.json_mock = patch('pedalparts.files.json').start()

        self.addCleanup(patch.stopall)

    def test_save_sets_path_of_file_to_save(self):
        save('file.json', [{'name': 1}])

        self.open_mock.assert_called_once_with('file.json', ANY)

    def test_save_opens_file_with_write_access(self):
        save('file.json', [{'name': 1}])

        self.open_mock.assert_called_once_with(ANY, 'w+')

    def test_data_is_written_as_json(self):
        data = [{'name': 1}]
        save('file.json', data)

        self.json_mock.dump.assert_called_once_with(data, ANY, indent=2)

    def test_data_is_written_with_open_file(self):
        save('file.json', [{'name': 1}])

        open_context_mock = self.open_mock.return_value \
            .__enter__.return_value

        self.json_mock.dump.assert_called_once_with(ANY, open_context_mock, indent=ANY)


class TestLoad(TestCase):
    def setUp(self):
        self.open_mock = patch('pedalparts.files.open').start()
        self.json_mock = patch('pedalparts.files.json').start()

        self.addCleanup(patch.stopall)

    def test_load_sets_path_to_file(self):
        load('file.json')

        self.open_mock.assert_called_once_with('file.json', ANY)

    def test_load_sets_read_permissions_for_open(self):
        load('file.json')

        self.open_mock.assert_called_once_with(ANY, 'r')

    def test_load_reads_file_as_json(self):
        load('file.json')

        open_context_mock = self.open_mock.return_value \
            .__enter__.return_value

        self.json_mock.load.assert_called_once_with(open_context_mock)

    def test_load_returns_loaded_json(self):
        self.json_mock.load.return_value = [{'name': 2}]

        result = load('file.json')

        self.assertEqual([{'name': 2}], result)

    def test_load_returns_empty_list_when_file_not_found(self):
        self.open_mock.side_effect = FileNotFoundError

        result = load('file.json')

        self.assertEqual([], result)
