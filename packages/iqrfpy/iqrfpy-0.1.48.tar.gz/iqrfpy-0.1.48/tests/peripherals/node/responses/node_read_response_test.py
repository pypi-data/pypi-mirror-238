import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import NodeResponseCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.node.responses.read import ReadResponse, NodeReadData
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': NodeMessages.READ,
    'msgid': 'readTest',
    'nadr': 1,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 85,
    'result': {
        'ntwADDR': 1,
        'ntwVRN': 1,
        'ntwZIN': 1,
        'ntwDID': 73,
        'ntwPVRN': 4,
        'ntwUSERADDRESS': 0,
        'ntwID': 188,
        'ntwVRNFNZ': 0,
        'ntwCFG': 2,
        'flags': 1
    },
    'dpa': b'\x01\x00\x01\x80\x02\x04\x00\x55\x01\x01\x01\x49\x04\x00\x00\xbc\x00\x00\x02\x01'
}

data_error: dict = {
    'mtype': NodeMessages.READ,
    'msgid': 'readTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 3,
    'dpa_value': 67,
    'dpa': b'\x00\x00\x01\x80\x00\x00\x03\x43'
}


class ReadResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, ReadResponse.from_dpa(data_ok['dpa']), False],
        ['from_json', data_ok, ReadResponse.from_json(generate_json_response(data_ok)), True],
        ['from_dpa_error', data_error, ReadResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, ReadResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.NODE)
        with self.subTest():
            self.assertEqual(response.pcmd, NodeResponseCommands.READ)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, NodeMessages.READ)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            ReadResponse.from_dpa(b'\x00\x00\x01\x80\x00\x00\x00\x47\x12\x02')

    @parameterized.expand([
        ['from_dpa', NodeReadData(data_ok['result']), ReadResponse.from_dpa(data_ok['dpa'])],
        ['from_json', NodeReadData(data_ok['result']), ReadResponse.from_json(generate_json_response(data_ok))]
    ])
    def test_get_node_data(self, _, data: NodeReadData, response: ReadResponse):
        self.assertEqual(response.node_data, data)

    @parameterized.expand([
        ['from_dpa_error', ReadResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', ReadResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_node_data_error(self, _, response: ReadResponse):
        self.assertIsNone(response.node_data)
