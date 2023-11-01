import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import CoordinatorResponseCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.coordinator.responses.set_dpa_params import SetDpaParamsResponse, DpaParam
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': CoordinatorMessages.SET_DPA_PARAMS,
    'msgid': 'setDpaParamsTest',
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 64,
    'result': {
        'prevDpaParam': DpaParam.LAST_RSSI,
    },
    'dpa': b'\x00\x00\x00\x88\x00\x00\x00\x40\x00'
}

data_ok_1: dict = {
    'mtype': CoordinatorMessages.SET_DPA_PARAMS,
    'msgid': 'setDpaParamsTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'result': {
        'prevDpaParam': DpaParam.USER_SPECIFIED,
    },
    'dpa': b'\x00\x00\x00\x88\x02\x04\x00\x23\x03'
}

data_error: dict = {
    'mtype': CoordinatorMessages.SET_DPA_PARAMS,
    'msgid': 'setDpaParamsTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x00\x88\x04\x04\x01\x23'
}


class SetDpaParamsResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, SetDpaParamsResponse.from_dpa(data_ok['dpa']), False],
        ['from_dpa', data_ok_1, SetDpaParamsResponse.from_dpa(data_ok_1['dpa']), False],
        ['from_json', data_ok, SetDpaParamsResponse.from_json(generate_json_response(data_ok)), True],
        ['from_json', data_ok_1, SetDpaParamsResponse.from_json(generate_json_response(data_ok_1)), True],
        ['from_dpa_error', data_error, SetDpaParamsResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, SetDpaParamsResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.COORDINATOR)
        with self.subTest():
            self.assertEqual(response.pcmd, CoordinatorResponseCommands.SET_DPA_PARAMS)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, CoordinatorMessages.SET_DPA_PARAMS)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(ValueError):
            SetDpaParamsResponse.from_dpa(b'\x00\x00\x00\x88\x00\x00\x00\x40')

    @parameterized.expand([
        ['from_dpa', data_ok['result']['prevDpaParam'], SetDpaParamsResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1['result']['prevDpaParam'], SetDpaParamsResponse.from_dpa(data_ok_1['dpa'])],
        ['from_json', data_ok['result']['prevDpaParam'], SetDpaParamsResponse.from_json(generate_json_response(data_ok))],
        ['from_json', data_ok_1['result']['prevDpaParam'], SetDpaParamsResponse.from_json(generate_json_response(data_ok_1))]
    ])
    def test_get_dpa_param(self, _, dpa_param: DpaParam, response: SetDpaParamsResponse):
        self.assertEqual(response.dpa_param, dpa_param)

    @parameterized.expand([
        ['from_dpa_error', SetDpaParamsResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', SetDpaParamsResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_dpa_param_error(self, _, response: SetDpaParamsResponse):
        self.assertIsNone(response.dpa_param)
