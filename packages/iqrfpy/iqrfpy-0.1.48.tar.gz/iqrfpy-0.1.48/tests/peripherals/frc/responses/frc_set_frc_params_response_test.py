import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import FrcResponseCommands
from iqrfpy.enums.message_types import FrcMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.frc.responses.set_frc_params import SetFrcParamsResponse
from iqrfpy.peripherals.frc.frc_params import FrcParams
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': FrcMessages.SET_PARAMS,
    'msgid': 'setFrcParamsTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 64,
    'result': {
        'frcResponseTime': 0,
    },
    'dpa': b'\x00\x00\x0d\x83\x00\x00\x00\x40\x00'
}

data_ok_1: dict = {
    'mtype': FrcMessages.SET_PARAMS,
    'msgid': 'setFrcParamsTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'result': {
        'frcResponseTime': 24,
    },
    'dpa': b'\x00\x00\x0d\x83\x02\x04\x00\x23\x18'
}

data_error: dict = {
    'mtype': FrcMessages.SET_PARAMS,
    'msgid': 'setFrcParamsTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x0d\x83\x04\x04\x01\x23'
}


class SetDpaParamsResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, SetFrcParamsResponse.from_dpa(data_ok['dpa']), False],
        ['from_dpa', data_ok_1, SetFrcParamsResponse.from_dpa(data_ok_1['dpa']), False],
        ['from_json', data_ok, SetFrcParamsResponse.from_json(generate_json_response(data_ok)), True],
        ['from_json', data_ok_1, SetFrcParamsResponse.from_json(generate_json_response(data_ok_1)), True],
        ['from_dpa_error', data_error, SetFrcParamsResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, SetFrcParamsResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.FRC)
        with self.subTest():
            self.assertEqual(response.pcmd, FrcResponseCommands.SET_PARAMS)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, FrcMessages.SET_PARAMS)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            SetFrcParamsResponse.from_dpa(b'\x00\x00\x0d\x83\x00\x00\x00\x40\x21\x05\x33')

    @parameterized.expand([
        [
            'from_dpa',
            FrcParams.from_int(data_ok['result']['frcResponseTime']),
            SetFrcParamsResponse.from_dpa(data_ok['dpa']),
        ],
        [
            'from_dpa',
            FrcParams.from_int(data_ok_1['result']['frcResponseTime']),
            SetFrcParamsResponse.from_dpa(data_ok_1['dpa']),
        ],
        [
            'from_json',
            FrcParams.from_int(data_ok['result']['frcResponseTime']),
            SetFrcParamsResponse.from_json(generate_json_response(data_ok)),
        ],
        [
            'from_json',
            FrcParams.from_int(data_ok_1['result']['frcResponseTime']),
            SetFrcParamsResponse.from_json(generate_json_response(data_ok_1)),
        ]
    ])
    def test_get_frc_params(self, _, frc_params: FrcParams, response: SetFrcParamsResponse):
        response_frc_params = response.frc_params
        with self.subTest():
            self.assertEqual(response_frc_params.offline_frc, frc_params.offline_frc)
        with self.subTest():
            self.assertEqual(response_frc_params.frc_response_time, frc_params.frc_response_time)

    @parameterized.expand([
        ['from_dpa_error', SetFrcParamsResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', SetFrcParamsResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_frc_params_error(self, _, response: SetFrcParamsResponse):
        self.assertIsNone(response.frc_params)
