import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import CoordinatorResponseCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.coordinator.responses.addr_info import AddrInfoResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': CoordinatorMessages.ADDR_INFO,
    'msgid': 'addrInfoTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 64,
    'result': {
        'devNr': 10,
        'did': 42,
    },
    'dpa': b'\x00\x00\x00\x80\x00\x00\x00\x40\x0a\x2a'
}

data_ok_1: dict = {
    'mtype': CoordinatorMessages.ADDR_INFO,
    'msgid': 'addrInfoTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'result': {
        'devNr': 5,
        'did': 42,
    },
    'dpa': b'\x00\x00\x00\x80\x02\x04\x00\x23\x05\x2a'
}

data_error: dict = {
    'mtype': CoordinatorMessages.ADDR_INFO,
    'msgid': 'addrInfoTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x00\x80\x04\x04\x01\x23'
}


class AddrInfoResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, AddrInfoResponse.from_dpa(data_ok['dpa']), False],
        ['from_dpa', data_ok_1, AddrInfoResponse.from_dpa(data_ok_1['dpa']), False],
        ['from_json', data_ok, AddrInfoResponse.from_json(generate_json_response(data_ok)), True],
        ['from_json', data_ok_1, AddrInfoResponse.from_json(generate_json_response(data_ok_1)), True],
        ['from_dpa_error', data_error, AddrInfoResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, AddrInfoResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.COORDINATOR)
        with self.subTest():
            self.assertEqual(response.pcmd, CoordinatorResponseCommands.ADDR_INFO)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, CoordinatorMessages.ADDR_INFO)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(ValueError):
            AddrInfoResponse.from_dpa(b'\x00\x00\x00\x80\x00\x00\x00\x40\x0a')

    @parameterized.expand([
        ['from_dpa', data_ok['result']['devNr'], AddrInfoResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1['result']['devNr'], AddrInfoResponse.from_dpa(data_ok_1['dpa'])],
        ['from_json', data_ok['result']['devNr'], AddrInfoResponse.from_json(generate_json_response(data_ok))],
        ['from_json', data_ok_1['result']['devNr'], AddrInfoResponse.from_json(generate_json_response(data_ok_1))]
    ])
    def test_get_dev_nr(self, _, dev_nr, response: AddrInfoResponse):
        self.assertEqual(response.dev_nr, dev_nr)

    @parameterized.expand([
        ['from_dpa_error', AddrInfoResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', AddrInfoResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_dev_nr_error(self, _, response: AddrInfoResponse):
        self.assertIsNone(response.dev_nr)

    @parameterized.expand([
        ['from_dpa', data_ok['result']['did'], AddrInfoResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1['result']['did'], AddrInfoResponse.from_dpa(data_ok_1['dpa'])],
        ['from_json', data_ok['result']['did'], AddrInfoResponse.from_json(generate_json_response(data_ok))],
        ['from_json', data_ok_1['result']['did'], AddrInfoResponse.from_json(generate_json_response(data_ok_1))]
    ])
    def test_get_did(self, _, did, response: AddrInfoResponse):
        self.assertEqual(response.did, did)

    @parameterized.expand([
        ['from_dpa_error', AddrInfoResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', AddrInfoResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_did_error(self, _, response: AddrInfoResponse):
        self.assertIsNone(response.did)
