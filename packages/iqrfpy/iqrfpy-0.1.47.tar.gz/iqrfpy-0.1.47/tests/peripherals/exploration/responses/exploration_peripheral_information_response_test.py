import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import ExplorationResponseCommands
from iqrfpy.enums.message_types import ExplorationMessages
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.exploration.responses.peripheral_information import PeripheralInformationResponse
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': ExplorationMessages.PERIPHERAL_INFORMATION,
    'msgid': 'peripheralInformationTest',
    'pnum': 2,
    'nadr': 3,
    'hwpid': 5122,
    'rcode': 0,
    'dpa_value': 79,
    'result': {
        'perTe': 3,
        'perT': 3,
        'par1': 3,
        'par2': 169,
    },
    'dpa': b'\x03\x00\x02\xbf\x02\x14\x00\x4f\x03\x03\x03\xa9'
}

data_error: dict = {
    'mtype': ExplorationMessages.PERIPHERAL_INFORMATION,
    'msgid': 'peripheralInformationTest',
    'pnum': 2,
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 7,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x02\xbf\x04\x04\x07\x23'
}


class PeripheralInformationResponseTestCase(unittest.TestCase):
    @parameterized.expand([
        ['from_dpa', data_ok, PeripheralInformationResponse.from_dpa(data_ok['dpa']), False],
        ['from_json', data_ok, PeripheralInformationResponse.from_json(generate_json_response(data_ok)), True],
        ['from_dpa_error', data_error, PeripheralInformationResponse.from_dpa(data_error['dpa']), False],
        [
            'from_json_error',
            data_error,
            PeripheralInformationResponse.from_json(
                generate_json_response(data_error)
            ),
            True,
        ]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, response_data['pnum'])
        with self.subTest():
            self.assertEqual(response.pcmd, ExplorationResponseCommands.PERIPHERALS_ENUMERATION_INFORMATION)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, ExplorationMessages.PERIPHERAL_INFORMATION)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            PeripheralInformationResponse.from_dpa(b'\x03\x00\x02\xbf\x02\x14\x00\x4f\x03')

    @parameterized.expand([
        ['from_dpa', data_ok['result']['perTe'], PeripheralInformationResponse.from_dpa(data_ok['dpa'])],
        [
            'from_json',
            data_ok['result']['perTe'],
            PeripheralInformationResponse.from_json(
                generate_json_response(data_ok)
            )
        ]
    ])
    def test_get_perte(self, _, perte: int, response: PeripheralInformationResponse):
        self.assertEqual(response.peripheral_data.perte, perte)

    @parameterized.expand([
        ['from_dpa', data_ok['result']['perT'], PeripheralInformationResponse.from_dpa(data_ok['dpa'])],
        [
            'from_json',
            data_ok['result']['perT'],
            PeripheralInformationResponse.from_json(
                generate_json_response(data_ok)
            )
        ]
    ])
    def test_get_pert(self, _, pert: int, response: PeripheralInformationResponse):
        self.assertEqual(response.peripheral_data.pert, pert)

    @parameterized.expand([
        ['from_dpa', data_ok['result']['par1'], PeripheralInformationResponse.from_dpa(data_ok['dpa'])],
        [
            'from_json',
            data_ok['result']['par1'],
            PeripheralInformationResponse.from_json(
                generate_json_response(data_ok)
            )
        ]
    ])
    def test_get_par1(self, _, par1: int, response: PeripheralInformationResponse):
        self.assertEqual(response.peripheral_data.par1, par1)

    @parameterized.expand([
        ['from_dpa', data_ok['result']['par2'], PeripheralInformationResponse.from_dpa(data_ok['dpa'])],
        [
            'from_json',
            data_ok['result']['par2'],
            PeripheralInformationResponse.from_json(
                generate_json_response(data_ok)
            )
        ]
    ])
    def test_get_par2(self, _, par2: int, response: PeripheralInformationResponse):
        self.assertEqual(response.peripheral_data.par2, par2)

    @parameterized.expand([
        ['from_dpa_error', PeripheralInformationResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', PeripheralInformationResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_peripheral_data_error(self, _, response: PeripheralInformationResponse):
        self.assertIsNone(response.peripheral_data)
