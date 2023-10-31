import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import CoordinatorResponseCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.coordinator.responses.authorize_bond import AuthorizeBondResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': CoordinatorMessages.AUTHORIZE_BOND,
    'msgid': 'authorizeBondTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 64,
    'result': {
        'bondAddr': 10,
        'devNr': 3
    },
    'dpa': b'\x00\x00\x00\x8d\x00\x00\x00\x40\x0a\x03'
}

data_ok_1: dict = {
    'mtype': CoordinatorMessages.AUTHORIZE_BOND,
    'msgid': 'authorizeBondTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'result': {
        'bondAddr': 7,
        'devNr': 1
    },
    'dpa': b'\x00\x00\x00\x8d\x02\x04\x00\x23\x07\x01'
}

data_error: dict = {
    'mtype': CoordinatorMessages.AUTHORIZE_BOND,
    'msgid': 'authorizeBondTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x00\x8d\x04\x04\x01\x23'
}


class AuthorizeBondResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, AuthorizeBondResponse.from_dpa(data_ok['dpa']), False],
        ['from_dpa', data_ok_1, AuthorizeBondResponse.from_dpa(data_ok_1['dpa']), False],
        ['from_json', data_ok, AuthorizeBondResponse.from_json(generate_json_response(data_ok)), True],
        ['from_json', data_ok_1, AuthorizeBondResponse.from_json(generate_json_response(data_ok_1)), True],
        ['from_dpa_error', data_error, AuthorizeBondResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, AuthorizeBondResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.COORDINATOR)
        with self.subTest():
            self.assertEqual(response.pcmd, CoordinatorResponseCommands.AUTHORIZE_BOND)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, CoordinatorMessages.AUTHORIZE_BOND)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(ValueError):
            AuthorizeBondResponse.from_dpa(b'\x00\x00\x00\x80\x00\x00\x00\x40\x0a')

    @parameterized.expand([
        ['from_dpa', data_ok['result']['bondAddr'], AuthorizeBondResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1['result']['bondAddr'], AuthorizeBondResponse.from_dpa(data_ok_1['dpa'])],
        ['from_json', data_ok['result']['bondAddr'], AuthorizeBondResponse.from_json(generate_json_response(data_ok))],
        ['from_json', data_ok_1['result']['bondAddr'], AuthorizeBondResponse.from_json(generate_json_response(data_ok_1))]
    ])
    def test_get_bond_addr(self, _, bond_addr, response: AuthorizeBondResponse):
        self.assertEqual(response.bond_addr, bond_addr)

    @parameterized.expand([
        ['from_dpa_error', AuthorizeBondResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', AuthorizeBondResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_bond_addr_error(self, _, response: AuthorizeBondResponse):
        self.assertIsNone(response.bond_addr)

    @parameterized.expand([
        ['from_dpa', data_ok['result']['devNr'], AuthorizeBondResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1['result']['devNr'], AuthorizeBondResponse.from_dpa(data_ok_1['dpa'])],
        ['from_json', data_ok['result']['devNr'], AuthorizeBondResponse.from_json(generate_json_response(data_ok))],
        ['from_json', data_ok_1['result']['devNr'], AuthorizeBondResponse.from_json(generate_json_response(data_ok_1))]
    ])
    def test_get_dev_nr(self, _, dev_nr, response: AuthorizeBondResponse):
        self.assertEqual(response.dev_nr, dev_nr)

    @parameterized.expand([
        ['from_dpa_error', AuthorizeBondResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', AuthorizeBondResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_dev_nr_error(self, _, response: AuthorizeBondResponse):
        self.assertIsNone(response.dev_nr)
