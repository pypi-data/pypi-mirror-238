import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import NodeResponseCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.node.responses.remove_bond import RemoveBondResponse
from iqrfpy.response_factory import ResponseFactory
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': NodeMessages.REMOVE_BOND,
    'msgid': 'removeBondTest',
    'nadr': 1,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 83,
    'dpa': b'\x01\x00\x01\x81\x02\x04\x00\x53'
}

data_error: dict = {
    'mtype': NodeMessages.REMOVE_BOND,
    'msgid': 'removeBondTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x01\x81\x02\x04\x01\x23'
}


class PulseResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, RemoveBondResponse.from_dpa(data_ok['dpa']), False],
        ['from_json', data_ok, RemoveBondResponse.from_json(generate_json_response(data_ok)), True],
        ['from_dpa_error', data_error, RemoveBondResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, RemoveBondResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.NODE)
        with self.subTest():
            self.assertEqual(response.pcmd, NodeResponseCommands.REMOVE_BOND)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, NodeMessages.REMOVE_BOND)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            ResponseFactory.get_response_from_dpa(b'\x01\x00\x01\x81\x00')
