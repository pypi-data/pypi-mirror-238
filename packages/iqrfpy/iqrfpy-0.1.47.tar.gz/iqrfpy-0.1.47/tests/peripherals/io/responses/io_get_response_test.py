import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import IOResponseCommands
from iqrfpy.enums.message_types import IOMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.io.responses import GetResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': IOMessages.GET.value,
    'msgid': 'getTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 90,
    'result': {
        'ports': [206, 81, 24, 0, 8]
    },
    'dpa': b'\x00\x00\x09\x82\x00\x00\x00\x5a\xce\x51\x18\x00\x08'
}

data_ok_1: dict = {
    'mtype': IOMessages.GET.value,
    'msgid': 'getTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'result': {
        'ports': [206, 81, 24, 0, 8]
    },
    'dpa': b'\x00\x00\x09\x82\x02\x04\x00\x23\xce\x51\x18\x00\x08'
}

data_error: dict = {
    'mtype': IOMessages.GET.value,
    'msgid': 'getTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 4,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x09\x82\x04\x04\x04\x23'
}


class ReadResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, GetResponse.from_dpa(data_ok['dpa']), False],
        ['from_dpa', data_ok_1, GetResponse.from_dpa(data_ok_1['dpa']), False],
        ['from_json', data_ok, GetResponse.from_json(generate_json_response(data_ok)), True],
        ['from_json', data_ok_1, GetResponse.from_json(generate_json_response(data_ok_1)), True],
        ['from_dpa_error', data_error, GetResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, GetResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.IO)
        with self.subTest():
            self.assertEqual(response.pcmd, IOResponseCommands.GET)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, IOMessages.GET)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    @parameterized.expand([
        ['from_dpa', data_ok['result']['ports'], GetResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1['result']['ports'], GetResponse.from_dpa(data_ok_1['dpa'])],
        ['from_json', data_ok['result']['ports'], GetResponse.from_json(generate_json_response(data_ok))],
        ['from_json', data_ok_1['result']['ports'], GetResponse.from_json(generate_json_response(data_ok_1))]
    ])
    def test_get_data(self, _, data, response: GetResponse):
        self.assertEqual(response.port_data, data)

    @parameterized.expand([
        ['from_dpa_error', GetResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', GetResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_port_data_error(self, _, response: GetResponse):
        self.assertIsNone(response.port_data)
