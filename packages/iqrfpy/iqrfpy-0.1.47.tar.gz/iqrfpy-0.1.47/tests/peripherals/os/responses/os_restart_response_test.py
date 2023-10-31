import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.os.responses.restart import RestartResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': OSMessages.RESTART,
    'msgid': 'restartTest',
    'nadr': 2,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 64,
    'dpa': b'\x02\x00\x02\x88\x00\x00\x00\x40'
}

data_ok_1: dict = {
    'mtype': OSMessages.RESTART,
    'msgid': 'restartTest',
    'nadr': 2,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'dpa': b'\x02\x00\x02\x88\x02\x04\x00\x23'
}

data_error: dict = {
    'mtype': OSMessages.RESTART,
    'msgid': 'restartTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 8,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x02\x88\x02\x04\x08\x23'
}


class RestartResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, RestartResponse.from_dpa(data_ok['dpa']), False],
        ['from_dpa', data_ok_1, RestartResponse.from_dpa(data_ok_1['dpa']), False],
        ['from_json', data_ok, RestartResponse.from_json(generate_json_response(data_ok)), True],
        ['from_json', data_ok_1, RestartResponse.from_json(generate_json_response(data_ok_1)), True],
        ['from_dpa_error', data_error, RestartResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, RestartResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.OS)
        with self.subTest():
            self.assertEqual(response.pcmd, OSResponseCommands.RESTART)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, OSMessages.RESTART)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            RestartResponse.from_dpa(b'\x02\x00\x02\x88\x00\x00\x00\x22\x32')
