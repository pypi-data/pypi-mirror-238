import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.os.responses.selective_batch import SelectiveBatchResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': OSMessages.SELECTIVE_BATCH,
    'msgid': 'selectiveBatchTest',
    'nadr': 1,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 64,
    'dpa': b'\x01\x00\x02\x85\x00\x00\x00\x40'
}

data_ok_1: dict = {
    'mtype': OSMessages.SELECTIVE_BATCH,
    'msgid': 'selectiveBatchTest',
    'nadr': 1,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'dpa': b'\x01\x00\x02\x85\x02\x04\x00\x23'
}

data_error: dict = {
    'mtype': OSMessages.SELECTIVE_BATCH,
    'msgid': 'selectiveBatchTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 3,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x02\x85\x02\x04\x03\x23'
}


class SelectiveBatchResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, SelectiveBatchResponse.from_dpa(data_ok['dpa']), False],
        ['from_dpa', data_ok_1, SelectiveBatchResponse.from_dpa(data_ok_1['dpa']), False],
        ['from_json', data_ok, SelectiveBatchResponse.from_json(generate_json_response(data_ok)), True],
        ['from_json', data_ok_1, SelectiveBatchResponse.from_json(generate_json_response(data_ok_1)), True],
        ['from_dpa_error', data_error, SelectiveBatchResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, SelectiveBatchResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.OS)
        with self.subTest():
            self.assertEqual(response.pcmd, OSResponseCommands.SELECTIVE_BATCH)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, OSMessages.SELECTIVE_BATCH)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            SelectiveBatchResponse.from_dpa(b'\x02\x00\x02\x85\x00\x00\x00\x22\x32')
