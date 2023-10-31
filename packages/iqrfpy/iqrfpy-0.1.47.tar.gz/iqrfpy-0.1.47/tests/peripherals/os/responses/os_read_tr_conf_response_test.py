import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.os.responses.read_tr_conf import ReadTrConfResponse, OsTrConfData
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': OSMessages.READ_CFG,
    'msgid': 'readTrConfTest',
    'nadr': 1,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 84,
    'result': {
        'checksum': 19,
        'configuration': [
           254,
           6,
           0,
           0,
           129,
           0,
           0,
           7,
           5,
           6,
           3,
           0,
           0,
           0,
           0,
           0,
           52,
           2,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           4,
           0
        ],
        'rfpgm': 195,
        'initphy': 48
    },
    'dpa': b'\x01\x00\x02\x82\x02\x04\x00\x54\x13\xfe\x06\x00\x00\x81\x00\x00\x07\x05\x06\x03\x00\x00\x00\x00\x00\x34'
           b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\xc3\x30'
}

data_error: dict = {
    'mtype': OSMessages.READ_CFG,
    'msgid': 'readTrConfTest',
    'nadr': 2,
    'hwpid': 1026,
    'rcode': 8,
    'dpa_value': 84,
    'dpa': b'\x02\x00\x02\x82\x02\x04\x08\x54'
}


class ReadTrConfResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, ReadTrConfResponse.from_dpa(data_ok['dpa']), False],
        [
            'from_json',
            data_ok,
            ReadTrConfResponse.from_json(
                generate_json_response(data_ok)
            ),
            True
        ],
        ['from_dpa_error', data_error, ReadTrConfResponse.from_dpa(data_error['dpa']), False],
        [
            'from_json_error',
            data_error,
            ReadTrConfResponse.from_json(
                generate_json_response(data_error)
            ),
            True
        ]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.OS)
        with self.subTest():
            self.assertEqual(response.pcmd, OSResponseCommands.READ_CFG)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, OSMessages.READ_CFG)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            ReadTrConfResponse.from_dpa(b'\x02\x00\x02\x82\x02\x04\x08')

    @parameterized.expand([
        [
            'from_dpa',
            data_ok['result']['checksum'],
            ReadTrConfResponse.from_dpa(data_ok['dpa'])
        ],
        [
            'from_json',
            data_ok['result']['checksum'],
            ReadTrConfResponse.from_json(
                generate_json_response(data_ok)
            )
        ]
    ])
    def test_get_checksum(self, _, data: int, response: ReadTrConfResponse):
        self.assertEqual(response.checksum, data)

    @parameterized.expand([
        ['from_dpa_error', ReadTrConfResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', ReadTrConfResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_checksum_error(self, _, response: ReadTrConfResponse):
        self.assertIsNone(response.checksum)

    @parameterized.expand([
        [
            'from_dpa',
            OsTrConfData.from_pdata(data_ok['result']['configuration']),
            ReadTrConfResponse.from_dpa(data_ok['dpa'])
        ],
        [
            'from_json',
            OsTrConfData.from_pdata(data_ok['result']['configuration']),
            ReadTrConfResponse.from_json(
                generate_json_response(data_ok)
            )
        ]
    ])
    def test_get_configuration(self, _, data: OsTrConfData, response: ReadTrConfResponse):
        self.assertEqual(response.configuration, data)

    @parameterized.expand([
        ['from_dpa_error', ReadTrConfResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', ReadTrConfResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_configuration_error(self, _, response: ReadTrConfResponse):
        self.assertIsNone(response.configuration)

    @parameterized.expand([
        [
            'from_dpa',
            data_ok['result']['rfpgm'],
            ReadTrConfResponse.from_dpa(data_ok['dpa'])
        ],
        [
            'from_json',
            data_ok['result']['rfpgm'],
            ReadTrConfResponse.from_json(
                generate_json_response(data_ok)
            )
        ]
    ])
    def test_get_rfpgm(self, _, data: int, response: ReadTrConfResponse):
        self.assertEqual(response.rfpgm, data)

    @parameterized.expand([
        ['from_dpa_error', ReadTrConfResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', ReadTrConfResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_rfpgm_error(self, _, response: ReadTrConfResponse):
        self.assertIsNone(response.rfpgm)

    @parameterized.expand([
        [
            'from_dpa',
            data_ok['result']['initphy'],
            ReadTrConfResponse.from_dpa(data_ok['dpa'])
        ],
        [
            'from_json',
            data_ok['result']['initphy'],
            ReadTrConfResponse.from_json(
                generate_json_response(data_ok)
            )
        ]
    ])
    def test_get_init_phy(self, _, data: int, response: ReadTrConfResponse):
        self.assertEqual(response.init_phy, data)

    @parameterized.expand([
        ['from_dpa_error', ReadTrConfResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', ReadTrConfResponse.from_json(generate_json_response(data_error))]
    ])
    def test_get_init_phy_error(self, _, response: ReadTrConfResponse):
        self.assertIsNone(response.init_phy)
