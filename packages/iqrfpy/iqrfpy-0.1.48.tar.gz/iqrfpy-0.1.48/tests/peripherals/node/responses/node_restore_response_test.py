import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import NodeResponseCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.node.responses.restore import RestoreResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': NodeMessages.RESTORE,
    'msgid': 'restoreTest',
    'nadr': 1,
    'hwpid': 2,
    'rcode': 0,
    'dpa_value': 64,
    'dpa': b'\x01\x00\x01\x87\x02\x00\x00\x40'
}

data_error: dict = {
    'mtype': NodeMessages.RESTORE,
    'msgid': 'restoreTest',
    'nadr': 1,
    'hwpid': 1028,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x01\x00\x01\x87\x04\x04\x01\x23'
}


class RestoreResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, RestoreResponse.from_dpa(data_ok['dpa']), False],
        ['from_json', data_ok, RestoreResponse.from_json(generate_json_response(data_ok)), True],
        ['from_dpa_error', data_error, RestoreResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, RestoreResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.NODE)
        with self.subTest():
            self.assertEqual(response.pcmd, NodeResponseCommands.RESTORE)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, NodeMessages.RESTORE)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            RestoreResponse.from_dpa(b'\x01\x00\x01\x87\x00\x00\x00\x22\x01')
