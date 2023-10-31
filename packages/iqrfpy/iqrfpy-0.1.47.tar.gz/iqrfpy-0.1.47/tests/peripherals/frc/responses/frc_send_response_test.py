import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.enums.commands import FrcResponseCommands
from iqrfpy.enums.message_types import FrcMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.frc.responses.send import SendResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': FrcMessages.SEND,
    'msgid': 'sendTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 64,
    'result': {
        'status': 3,
        'frcData': [0, 27, 27, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    'dpa': b'\x00\x00\x0d\x80\x00\x00\x00\x00\x03\x00\x1b\x1b\x1a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
}

data_error: dict = {
    'mtype': FrcMessages.SEND,
    'msgid': 'sendTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x00\x80\x04\x04\x01\x23'
}


class ExtraResultResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, SendResponse.from_dpa(data_ok['dpa']), False],
        ['from_json', data_ok, SendResponse.from_json(generate_json_response(data_ok)), True],
        ['from_dpa_error', data_error, SendResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, SendResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.FRC)
        with self.subTest():
            self.assertEqual(response.pcmd, FrcResponseCommands.SEND)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, FrcMessages.SEND)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            SendResponse.from_dpa(b'\x00\x00\x0d\x80\x00\x00\x00\x40\x0a')

    @parameterized.expand([
        ['from_dpa', data_ok['result']['status'], SendResponse.from_dpa(data_ok['dpa'])],
        ['from_json', data_ok['result']['status'], SendResponse.from_json(generate_json_response(data_ok))],
    ])
    def test_get_status(self, _, status: int, response: SendResponse):
        self.assertEqual(response.status, status)

    @parameterized.expand([
        ['from_dpa_error', SendResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', SendResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_status_error(self, _, response: SendResponse):
        self.assertIsNone(response.status)

    @parameterized.expand([
        ['from_dpa', data_ok['result']['frcData'], SendResponse.from_dpa(data_ok['dpa'])],
        ['from_json', data_ok['result']['frcData'], SendResponse.from_json(generate_json_response(data_ok))],
    ])
    def test_get_frc_data(self, _, frc_data: List[int], response: SendResponse):
        self.assertEqual(response.frc_data, frc_data)

    @parameterized.expand([
        ['from_dpa_error', SendResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', SendResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_frc_data_error(self, _, response: SendResponse):
        self.assertIsNone(response.frc_data)
