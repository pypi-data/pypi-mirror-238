import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import IOResponseCommands
from iqrfpy.enums.message_types import IOMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.io.responses import DirectionResponse
from iqrfpy.response_factory import ResponseFactory
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': IOMessages.DIRECTION.value,
    'msgid': 'directionTest',
    'nadr': 1,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 67,
    'dpa': b'\x01\x00\x09\x80\x00\x00\x00\x43'
}

data_ok_1: dict = {
    'mtype': IOMessages.DIRECTION.value,
    'msgid': 'directionTest',
    'nadr': 2,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'dpa': b'\x02\x00\x09\x80\x02\x04\x00\x23'
}

data_error: dict = {
    'mtype': IOMessages.DIRECTION.value,
    'msgid': 'directionTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 3,
    'dpa_value': 0,
    'dpa': b'\x00\x00\x09\x80\x00\x00\x03\x00'
}


class DirectionResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, DirectionResponse.from_dpa(data_ok['dpa']), False],
        ['from_dpa', data_ok_1, ResponseFactory.get_response_from_dpa(data_ok_1['dpa']), False],
        ['from_json', data_ok, DirectionResponse.from_json(generate_json_response(data_ok)), True],
        ['from_json', data_ok_1, ResponseFactory.get_response_from_json(generate_json_response(data_ok_1)), True],
        ['from_dpa_error', data_error, ResponseFactory.get_response_from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, ResponseFactory.get_response_from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.IO)
        with self.subTest():
            self.assertEqual(response.pcmd, IOResponseCommands.DIRECTION)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, IOMessages.DIRECTION)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(ValueError):
            ResponseFactory.get_response_from_dpa(b'\x01\x00\x09\x80\x00\x00\x00\x22\x32')
