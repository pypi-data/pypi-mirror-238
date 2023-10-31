import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.enums.commands import ExplorationResponseCommands
from iqrfpy.enums.message_types import ExplorationMessages
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.exploration.responses.peripheral_information_data import PeripheralInformationData
from iqrfpy.peripherals.exploration.responses.more_peripherals_information import MorePeripheralsInformationResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': ExplorationMessages.MORE_PERIPHERALS_INFORMATION,
    'msgid': 'morePeripheralsInformationTest',
    'pcmd': 128,
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 0,
    'result': {
        "peripherals": [
            {
                "perTe": 3,
                "perT": 1,
                "par1": 56,
                "par2": 0
            },
            {
                "perTe": 3,
                "perT": 0,
                "par1": 0,
                "par2": 0
            },
            {
                "perTe": 3,
                "perT": 3,
                "par1": 36,
                "par2": 194
            },
            {
                "perTe": 3,
                "perT": 4,
                "par1": 64,
                "par2": 55
            },
            {
                "perTe": 3,
                "perT": 5,
                "par1": 128,
                "par2": 0
            },
            {
                "perTe": 3,
                "perT": 6,
                "par1": 48,
                "par2": 48
            },
            {
                "perTe": 3,
                "perT": 7,
                "par1": 0,
                "par2": 0
            },
            {
                "perTe": 3,
                "perT": 7,
                "par1": 1,
                "par2": 0
            },
            {
                "perTe": 3,
                "perT": 0,
                "par1": 0,
                "par2": 0
            },
            {
                "perTe": 3,
                "perT": 9,
                "par1": 23,
                "par2": 0
            },
            {
                "perTe": 1,
                "perT": 11,
                "par1": 0,
                "par2": 0
            },
            {
                "perTe": 3,
                "perT": 0,
                "par1": 0,
                "par2": 0
            },
            {
                "perTe": 3,
                "perT": 0,
                "par1": 0,
                "par2": 0
            },
            {
                "perTe": 3,
                "perT": 14,
                "par1": 55,
                "par2": 0
            }
        ]
    },
    'dpa': b'\x00\x00\xff\x80\x00\x00\x00\x00\x03\x01\x38\x00\x03\x00\x00\x00\x03\x03\x24\xc2\x03\x04\x40\x37\x03\x05'
           b'\x80\x00\x03\x06\x30\x30\x03\x07\x00\x00\x03\x07\x01\x00\x03\x00\x00\x00\x03\x09\x17\x00\x01\x0b\x00\x00'
           b'\x03\x00\x00\x00\x03\x00\x00\x00\x03\x0e\x37\x00'
}

data_error: dict = {
    'mtype': ExplorationMessages.MORE_PERIPHERALS_INFORMATION,
    'msgid': 'morePeripheralInformationTest',
    'nadr': 0,
    'pcmd': 128,
    'hwpid': 1028,
    'rcode': 7,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x02\x80\x04\x04\x07\x23'
}


class MorePeripheralsInformationResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, MorePeripheralsInformationResponse.from_dpa(data_ok['dpa']), False],
        ['from_json', data_ok, MorePeripheralsInformationResponse.from_json(generate_json_response(data_ok)), True],
        ['from_dpa_error', data_error, MorePeripheralsInformationResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, MorePeripheralsInformationResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, ExplorationResponseCommands.MORE_PERIPHERALS_INFORMATION)
        with self.subTest():
            self.assertEqual(response.pcmd, response_data['pcmd'])
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, ExplorationMessages.MORE_PERIPHERALS_INFORMATION)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    @parameterized.expand([
        [b'\x00\x00\xff\x80\x00\x00'],
        [b'\x00\x00\xff\x80\x00\x00\x00\x00\x03\x01\x38\x00\x03\x00\x00']
    ])
    def test_from_dpa_invalid(self, dpa: bytes):
        with self.assertRaises(DpaResponsePacketLengthError):
            MorePeripheralsInformationResponse.from_dpa(dpa=dpa)

    @parameterized.expand([
        [
            'from_dpa',
            [PeripheralInformationData(x) for x in data_ok['result']['peripherals']],
            MorePeripheralsInformationResponse.from_dpa(data_ok['dpa'])
        ],
        [
            'from_json',
            [PeripheralInformationData(x) for x in data_ok['result']['peripherals']],
            MorePeripheralsInformationResponse.from_json(generate_json_response(data_ok))
        ]
    ])
    def test_get_peripheral_data(self, _, peripheral_data: List[PeripheralInformationData],
                                 response: MorePeripheralsInformationResponse):
        self.assertEqual(peripheral_data, response.peripheral_data)

    @parameterized.expand([
        ['from_dpa_error', MorePeripheralsInformationResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', MorePeripheralsInformationResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_peripheral_data_error(self, _, response: MorePeripheralsInformationResponse):
        self.assertIsNone(response.peripheral_data)
