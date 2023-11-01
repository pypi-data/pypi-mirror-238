import unittest
from typing import List, Union
from parameterized import parameterized
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.os.requests.write_tr_conf import WriteTrConfRequest, OsTrConfData


class WriteTrConfRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x02\x0f\xff\xff\x00\xfe\x06\x00\x00\x81\x00\x00\x07\x05\x06\x03\x00\x00\x00\x00' \
                   b'\x00\x34\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\xc3'
        self.json = {
            'mType': 'iqrfEmbedOs_WriteCfg',
            'data': {
                'msgId': 'writeTrConfTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'checksum': 0,
                        'configuration': [254, 6, 0, 0, 129, 0, 0, 7, 5, 6, 3, 0, 0, 0, 0, 0, 52, 2, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 4, 0],
                        'rfpgm': 195
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            OsTrConfData(
                embedded_peripherals=[
                    EmbedPeripherals.NODE,
                    EmbedPeripherals.OS,
                    EmbedPeripherals.EEPROM,
                    EmbedPeripherals.EEEPROM,
                    EmbedPeripherals.RAM,
                    EmbedPeripherals.LEDR,
                    EmbedPeripherals.LEDG,
                    EmbedPeripherals.IO,
                    EmbedPeripherals.THERMOMETER
                ],
                custom_dpa_handler=True,
                std_and_lp_network=True,
                rf_output_power=7,
                rf_signal_filter=5,
                lp_rf_timeout=6,
                uart_baud_rate=3,
                rf_channel_a=52,
                rf_channel_b=2,
                reserved_block_0=[0, 0],
                reserved_block_1=[0, 0, 0],
                reserved_block_2=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0]
            )
        ],
        [
            OsTrConfData.from_pdata(
                [254, 6, 0, 0, 129, 0, 0, 7, 5, 6, 3, 0, 0, 0, 0, 0, 52, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0]
            )
        ]
    ])
    def test_to_dpa(self, configuration: Union[OsTrConfData, List[int]]):
        request = WriteTrConfRequest(nadr=1, configuration=configuration, rfpgm=195)
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )

    @parameterized.expand([
        [
            OsTrConfData(
                embedded_peripherals=[
                    EmbedPeripherals.NODE,
                    EmbedPeripherals.OS,
                    EmbedPeripherals.EEPROM,
                    EmbedPeripherals.EEEPROM,
                    EmbedPeripherals.RAM,
                    EmbedPeripherals.LEDR,
                    EmbedPeripherals.LEDG,
                    EmbedPeripherals.IO,
                    EmbedPeripherals.THERMOMETER
                ],
                custom_dpa_handler=True,
                std_and_lp_network=True,
                rf_output_power=7,
                rf_signal_filter=5,
                lp_rf_timeout=6,
                uart_baud_rate=3,
                rf_channel_a=52,
                rf_channel_b=2,
                reserved_block_0=[0, 0],
                reserved_block_1=[0, 0, 0],
                reserved_block_2=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0]
            )
        ],
        [
            OsTrConfData.from_pdata(
                [254, 6, 0, 0, 129, 0, 0, 7, 5, 6, 3, 0, 0, 0, 0, 0, 52, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0]
            )
        ]
    ])
    def test_to_json(self, configuration: Union[OsTrConfData, List[int]]):
        request = WriteTrConfRequest(nadr=1, configuration=configuration, rfpgm=195, msgid='writeTrConfTest')
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [OsTrConfData()]
    ])
    def test_set_configuration(self, configuration):
        request = WriteTrConfRequest(nadr=1, configuration=OsTrConfData.from_pdata(
            self.json['data']['req']['param']['configuration']), rfpgm=195, msgid='writeTrConfTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.configuration = configuration
        self.json['data']['req']['param']['configuration'] = configuration.to_pdata()
        dpa = self.dpa[:7] + bytes(configuration.to_pdata()) + bytes([self.dpa[len(self.dpa) - 1]])
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [10],
        [155],
        [195]
    ])
    def test_set_rfpgm(self, rfpgm: int):
        request = WriteTrConfRequest(nadr=1, configuration=OsTrConfData.from_pdata(
            self.json['data']['req']['param']['configuration']), rfpgm=195, msgid='writeTrConfTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.rfpgm = rfpgm
        self.json['data']['req']['param']['rfpgm'] = rfpgm
        dpa = self.dpa[:-1] + bytes([rfpgm])
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [[-1]],
        [[0] * 33],
        [[256]]
    ])
    def test_invalid_embedded_peripherals(self, embedded_peripherals):
        with self.assertRaises(RequestParameterInvalidValueError):
            OsTrConfData(embedded_peripherals=embedded_peripherals)

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_rf_output_power(self, rf_output_power):
        with self.assertRaises(RequestParameterInvalidValueError):
            OsTrConfData(rf_output_power=rf_output_power)

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_rf_signal_filter(self, rf_signal_filter):
        with self.assertRaises(RequestParameterInvalidValueError):
            OsTrConfData(rf_signal_filter=rf_signal_filter)

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_lp_rf_timeout(self, lp_rf_timeout):
        with self.assertRaises(RequestParameterInvalidValueError):
            OsTrConfData(lp_rf_timeout=lp_rf_timeout)

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_uart_baud_rate(self, uart_baud_rate):
        with self.assertRaises(RequestParameterInvalidValueError):
            OsTrConfData(uart_baud_rate=uart_baud_rate)

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_alternative_dsm_channel(self, alternative_dsm_channel):
        with self.assertRaises(RequestParameterInvalidValueError):
            OsTrConfData(alternative_dsm_channel=alternative_dsm_channel)

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_rf_channel_a(self, rf_channel_a):
        with self.assertRaises(RequestParameterInvalidValueError):
            OsTrConfData(rf_channel_a=rf_channel_a)

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_rf_channel_b(self, rf_channel_b):
        with self.assertRaises(RequestParameterInvalidValueError):
            OsTrConfData(rf_channel_b=rf_channel_b)

    @parameterized.expand([
        [[-1] * 2],
        [[256] * 2],
        [[0]]
    ])
    def test_invalid_reserved_block_0(self, data: List[int]):
        with self.assertRaises(RequestParameterInvalidValueError):
            OsTrConfData(reserved_block_0=data)

    @parameterized.expand([
        [[-1] * 3],
        [[256] * 3],
        [[0]]
    ])
    def test_invalid_reserved_block_1(self, data: List[int]):
        with self.assertRaises(RequestParameterInvalidValueError):
            OsTrConfData(reserved_block_1=data)

    @parameterized.expand([
        [[-1] * 13],
        [[256] * 13],
        [[0]]
    ])
    def test_invalid_reserved_block_2(self, data: List[int]):
        with self.assertRaises(RequestParameterInvalidValueError):
            OsTrConfData(reserved_block_2=data)

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_rfpgm(self, rfpgm):
        with self.assertRaises(RequestParameterInvalidValueError):
            WriteTrConfRequest(nadr=1, configuration=OsTrConfData(), rfpgm=rfpgm)
