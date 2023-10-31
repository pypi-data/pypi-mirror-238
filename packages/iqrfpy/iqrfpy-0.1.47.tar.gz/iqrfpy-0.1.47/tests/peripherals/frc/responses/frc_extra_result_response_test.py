import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.enums.commands import FrcResponseCommands
from iqrfpy.enums.message_types import FrcMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.frc.responses.extra_result import ExtraResultResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': FrcMessages.EXTRA_RESULT,
    'msgid': 'extraResultTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 64,
    'result': {
        'frcData': [0] * 9
    },
    'dpa': b'\x00\x00\x0d\x81\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00'
}

data_ok_1: dict = {
    'mtype': FrcMessages.EXTRA_RESULT,
    'msgid': 'extraResultTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'result': {
        'frcData': [17, 20, 0, 14, 1, 2, 7, 8, 255]
    },
    'dpa': b'\x00\x00\x0d\x81\x02\x04\x00\x23\x11\x14\x00\x0e\x01\x02\x07\x08\xff'
}

data_error: dict = {
    'mtype': FrcMessages.EXTRA_RESULT,
    'msgid': 'extraResultTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x00\x80\x04\x04\x01\x23'
}


class ExtraResultResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, ExtraResultResponse.from_dpa(data_ok['dpa']), False],
        ['from_dpa', data_ok_1, ExtraResultResponse.from_dpa(data_ok_1['dpa']), False],
        ['from_json', data_ok, ExtraResultResponse.from_json(generate_json_response(data_ok)), True],
        ['from_json', data_ok_1, ExtraResultResponse.from_json(generate_json_response(data_ok_1)), True],
        ['from_dpa_error', data_error, ExtraResultResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, ExtraResultResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.FRC)
        with self.subTest():
            self.assertEqual(response.pcmd, FrcResponseCommands.EXTRA_RESULT)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, FrcMessages.EXTRA_RESULT)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            ExtraResultResponse.from_dpa(b'\x00\x00\x0d\x81\x00\x00\x00\x40\x0a')

    @parameterized.expand([
        ['from_dpa', data_ok['result']['frcData'], ExtraResultResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1['result']['frcData'], ExtraResultResponse.from_dpa(data_ok_1['dpa'])],
        ['from_json', data_ok['result']['frcData'], ExtraResultResponse.from_json(generate_json_response(data_ok))],
        ['from_json', data_ok_1['result']['frcData'], ExtraResultResponse.from_json(generate_json_response(data_ok_1))]
    ])
    def test_get_frc_data(self, _, frc_data: List[int], response: ExtraResultResponse):
        self.assertEqual(response.frc_data, frc_data)

    @parameterized.expand([
        ['from_dpa_error', ExtraResultResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', ExtraResultResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_frc_data_error(self, _, response: ExtraResultResponse):
        self.assertIsNone(response.frc_data)
