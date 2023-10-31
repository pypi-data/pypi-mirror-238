import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import CoordinatorResponseCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.coordinator.responses.discovery import DiscoveryResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': CoordinatorMessages.DISCOVERY,
    'msgid': 'discoveryTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 55,
    'result': {
        'discNr': 15
    },
    'dpa': b'\x00\x00\x00\x87\x00\x00\x00\x37\x0f'

}

data_ok_1: dict = {
    'mtype': CoordinatorMessages.DISCOVERY,
    'msgid': 'discoveryTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'result': {
        'discNr': 3
    },
    'dpa': b'\x00\x00\x00\x87\x02\x04\x00\x23\x03'
}

data_error: dict = {
    'mtype': CoordinatorMessages.DISCOVERY,
    'msgid': 'discoveryTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 7,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x00\x87\x04\x04\x07\x23'
}


class DiscoveryResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, DiscoveryResponse.from_dpa(data_ok['dpa']), False],
        ['from_dpa', data_ok_1, DiscoveryResponse.from_dpa(data_ok_1['dpa']), False],
        ['from_json', data_ok, DiscoveryResponse.from_json(generate_json_response(data_ok)), True],
        ['from_json', data_ok_1, DiscoveryResponse.from_json(generate_json_response(data_ok_1)), True],
        ['from_dpa_error', data_error, DiscoveryResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, DiscoveryResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.COORDINATOR)
        with self.subTest():
            self.assertEqual(response.pcmd, CoordinatorResponseCommands.DISCOVERY)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, CoordinatorMessages.DISCOVERY)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(ValueError):
            DiscoveryResponse.from_dpa(b'\x00\x00\x00\x87\x00\x00\x00\x22')

    @parameterized.expand([
        ['from_dpa', data_ok['result']['discNr'], DiscoveryResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1['result']['discNr'], DiscoveryResponse.from_dpa(data_ok_1['dpa'])],
        ['from_json', data_ok['result']['discNr'], DiscoveryResponse.from_json(generate_json_response(data_ok))],
        ['from_json', data_ok_1['result']['discNr'], DiscoveryResponse.from_json(generate_json_response(data_ok_1))]
    ])
    def test_get_disc_nr(self, _, disc_nr, response: DiscoveryResponse):
        self.assertEqual(response.disc_nr, disc_nr)

    @parameterized.expand([
        ['from_dpa_error', DiscoveryResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', DiscoveryResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_disc_nr_error(self, _, response: DiscoveryResponse):
        self.assertIsNone(response.disc_nr)
