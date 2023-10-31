import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import NodeResponseCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.node.responses.backup import BackupResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': NodeMessages.BACKUP,
    'msgid': 'backupTest',
    'nadr': 1,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 81,
    'result': {
        'backupData': [118, 141, 15, 207, 51, 118, 253, 211, 77, 1, 57, 187, 185, 27, 251, 200, 192, 106, 183, 80, 136,
                       142, 134, 92, 157, 69, 114, 33, 102, 98, 56, 230, 194, 61, 161, 152, 107, 233, 102, 228, 247,
                       134, 72, 37, 246, 216, 175, 188, 6]
    },
    'dpa': b'\x01\x00\x01\x86\x02\x04\x00\x51\x76\x8d\x0f\xcf\x33\x76\xfd\xd3\x4d\x01\x39\xbb\xb9\x1b\xfb\xc8\xc0\x6a'
           b'\xb7\x50\x88\x8e\x86\x5c\x9d\x45\x72\x21\x66\x62\x38\xe6\xc2\x3d\xa1\x98\x6b\xe9\x66\xe4\xf7\x86\x48\x25'
           b'\xf6\xd8\xaf\xbc\x06'
}

data_error: dict = {
    'mtype': NodeMessages.BACKUP,
    'msgid': 'backupTest',
    'nadr': 1,
    'hwpid': 1028,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x01\x00\x01\x86\x04\x04\x01\x23'
}


class BackupResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, BackupResponse.from_dpa(data_ok['dpa']), False],
        ['from_json', data_ok, BackupResponse.from_json(generate_json_response(data_ok)), True],
        ['from_dpa_error', data_error, BackupResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, BackupResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.NODE)
        with self.subTest():
            self.assertEqual(response.pcmd, NodeResponseCommands.BACKUP)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, NodeMessages.BACKUP)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(ValueError):
            BackupResponse.from_dpa(b'\x01\x00\x01\x81\x00\x00\x00\x40')

    @parameterized.expand([
        ['from_dpa', data_ok['result']['backupData'], BackupResponse.from_dpa(data_ok['dpa'])],
        ['from_json', data_ok['result']['backupData'], BackupResponse.from_json(generate_json_response(data_ok))]
    ])
    def test_get_backup_data(self, _, backup_data, response: BackupResponse):
        self.assertEqual(response.backup_data, backup_data)

    @parameterized.expand([
        ['from_dpa_error', BackupResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', BackupResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_backup_data_error(self, _, response: BackupResponse):
        self.assertIsNone(response.backup_data)
