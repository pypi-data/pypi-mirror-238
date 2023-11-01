import random
import unittest
from typing import Union

from parameterized import parameterized

from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.os.requests.tr_conf_byte import OsTrConfByte
from iqrfpy.peripherals.os.os_tr_conf_data import OsTrConfData
from iqrfpy.utils.dpa import TrConfByteAddrs, TrConfBitMasks


class OsTrConfDataTest(unittest.TestCase):

    def setUp(self) -> None:
        self.conf = OsTrConfData(
            embedded_peripherals=[
                EmbedPeripherals.COORDINATOR,
                2,
                EmbedPeripherals.EEPROM,
                EmbedPeripherals.EEEPROM,
                5,
                EmbedPeripherals.LEDR,
                EmbedPeripherals.IO,
                EmbedPeripherals.THERMOMETER,
                13,
            ],
            custom_dpa_handler=False,
            dpa_peer_to_peer=False,
            routing_off=False,
            io_setup=False,
            user_peer_to_peer=False,
            stay_awake_when_not_bonded=True,
            std_and_lp_network=True,
            rf_output_power=7,
            rf_signal_filter=5,
            lp_rf_timeout=30,
            uart_baud_rate=6,
            alternative_dsm_channel=20,
            local_frc=False,
            rf_channel_a=52,
            rf_channel_b=1,
            reserved_block_0=[0, 0],
            reserved_block_1=[0, 0, 0],
            reserved_block_2=[0] * 13
        )

    def test_get_embedded_peripherals(self):
        self.assertEqual(self.conf.embedded_peripherals, [0, 2, 3, 4, 5, 6, 9, 10, 13])

    def test_set_embedded_peripherals(self):
        peripherals = [1, 2, 3, 4, 5, 6, 10]
        self.conf.embedded_peripherals = peripherals
        self.assertListEqual(
            self.conf.embedded_peripherals,
            [
                EmbedPeripherals.NODE,
                EmbedPeripherals.OS,
                EmbedPeripherals.EEPROM,
                EmbedPeripherals.EEEPROM,
                EmbedPeripherals.RAM,
                EmbedPeripherals.LEDR,
                EmbedPeripherals.THERMOMETER
            ]
        )

    @parameterized.expand([
        [7],
        [EmbedPeripherals.LEDG],
        [12],
        [EmbedPeripherals.UART],
    ])
    def test_enable_embedded_peripheral(self, peripheral: Union[EmbedPeripherals, int]):
        self.assertFalse(peripheral in self.conf.embedded_peripherals)
        self.conf.enable_embedded_peripheral(peripheral)
        self.assertTrue(peripheral in self.conf.embedded_peripherals)

    @parameterized.expand([
        [-1],
        [32],
        [255],
    ])
    def test_enable_embedded_peripheral_invalid(self, peripheral: int):
        with self.assertRaises(ValueError):
            self.conf.enable_embedded_peripheral(peripheral)

    @parameterized.expand([
        [0],
        [EmbedPeripherals.COORDINATOR],
        [2],
        [EmbedPeripherals.OS],
    ])
    def test_disable_embedded_peripheral(self, peripheral: Union[EmbedPeripherals, int]):
        self.assertTrue(peripheral in self.conf.embedded_peripherals)
        self.conf.disable_embedded_peripheral(peripheral)
        self.assertFalse(peripheral in self.conf.embedded_peripherals)

    @parameterized.expand([
        [-1],
        [32],
        [255],
    ])
    def test_disable_embedded_peripheral_invalid(self, peripheral: int):
        with self.assertRaises(ValueError):
            self.conf.disable_embedded_peripheral(peripheral)

    @parameterized.expand([
        [
            EmbedPeripherals.COORDINATOR,
            OsTrConfByte(
                address=1,
                value=1,
                mask=1
            )
        ],
        [
            EmbedPeripherals.LEDR,
            OsTrConfByte(
                address=1,
                value=64,
                mask=64
            )
        ],
        [
            EmbedPeripherals.THERMOMETER,
            OsTrConfByte(
                address=2,
                value=4,
                mask=4
            )
        ],
        [
            23,
            OsTrConfByte(
                address=3,
                value=0,
                mask=0
            )
        ],
        [
            31,
            OsTrConfByte(
                address=4,
                value=0,
                mask=0
            )
        ]
    ])
    def test_get_embedded_peripheral_byte(self, peripheral: Union[EmbedPeripherals, int], byte: OsTrConfByte):
        self.assertEqual(
            self.conf.get_embedded_peripheral_byte(peripheral),
            byte
        )

    @parameterized.expand([
        [-1],
        [32],
        [255],
    ])
    def test_get_embedded_peripheral_byte_invalid(self, peripheral: int):
        with self.assertRaises(ValueError):
            self.conf.get_embedded_peripheral_byte(peripheral)

    def test_custom_dpa_handler(self):
        self.assertFalse(self.conf.custom_dpa_handler)
        self.conf.custom_dpa_handler = True
        self.assertTrue(self.conf.custom_dpa_handler)

    @parameterized.expand([
        [
            False,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=0,
                mask=TrConfBitMasks.CUSTOM_DPA_HANDLER
            )
        ],
        [
            True,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=1,
                mask=TrConfBitMasks.CUSTOM_DPA_HANDLER
            )
        ]
    ])
    def test_get_custom_dpa_handler_byte(self, value: bool, expected: OsTrConfByte):
        self.conf.custom_dpa_handler = value
        self.assertEqual(
            self.conf.get_custom_dpa_handler_byte(),
            expected
        )

    def test_dpa_peer_to_peer(self):
        self.assertFalse(self.conf.dpa_peer_to_peer)
        self.conf.dpa_peer_to_peer = True
        self.assertTrue(self.conf.dpa_peer_to_peer)

    @parameterized.expand([
        [
            False,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=0,
                mask=TrConfBitMasks.DPA_PEER_TO_PEER
            )
        ],
        [
            True,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=2,
                mask=TrConfBitMasks.DPA_PEER_TO_PEER
            )
        ]
    ])
    def test_get_dpa_peer_to_peer_byte(self, value: bool, expected: OsTrConfByte):
        self.conf.dpa_peer_to_peer = value
        self.assertEqual(
            self.conf.get_dpa_peer_to_peer_byte(),
            expected
        )

    def test_routing_off(self):
        self.assertFalse(self.conf.routing_off)
        self.conf.routing_off = True
        self.assertTrue(self.conf.routing_off)

    @parameterized.expand([
        [
            False,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=0,
                mask=TrConfBitMasks.ROUTING_OFF
            )
        ],
        [
            True,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=8,
                mask=TrConfBitMasks.ROUTING_OFF
            )
        ]
    ])
    def test_get_routing_off_byte(self, value: bool, expected: OsTrConfByte):
        self.conf.routing_off = value
        self.assertEqual(
            self.conf.get_routing_off_byte(),
            expected
        )

    def test_io_setup(self):
        self.assertFalse(self.conf.io_setup)
        self.conf.io_setup = True
        self.assertTrue(self.conf.io_setup)

    @parameterized.expand([
        [
            False,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=0,
                mask=TrConfBitMasks.IO_SETUP
            )
        ],
        [
            True,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=16,
                mask=TrConfBitMasks.IO_SETUP
            )
        ]
    ])
    def test_get_io_setup_byte(self, value: bool, expected: OsTrConfByte):
        self.conf.io_setup = value
        self.assertEqual(
            self.conf.get_io_setup_byte(),
            expected
        )

    def test_user_peer_to_peer(self):
        self.assertFalse(self.conf.user_peer_to_peer)
        self.conf.user_peer_to_peer = True
        self.assertTrue(self.conf.user_peer_to_peer)

    @parameterized.expand([
        [
            False,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=0,
                mask=TrConfBitMasks.USER_PEER_TO_PEER
            )
        ],
        [
            True,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=32,
                mask=TrConfBitMasks.USER_PEER_TO_PEER
            )
        ]
    ])
    def test_get_user_peer_to_peer_byte(self, value: bool, expected: OsTrConfByte):
        self.conf.user_peer_to_peer = value
        self.assertEqual(
            self.conf.get_user_peer_to_peer_byte(),
            expected
        )

    def test_stay_awake_when_not_bonded(self):
        self.assertTrue(self.conf.stay_awake_when_not_bonded)
        self.conf.stay_awake_when_not_bonded = False
        self.assertFalse(self.conf.stay_awake_when_not_bonded)

    @parameterized.expand([
        [
            False,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=0,
                mask=TrConfBitMasks.STAY_AWAKE_WHEN_NOT_BONDED
            )
        ],
        [
            True,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=64,
                mask=TrConfBitMasks.STAY_AWAKE_WHEN_NOT_BONDED
            )
        ]
    ])
    def test_get_stay_awake_when_not_bonded_byte(self, value: bool, expected: OsTrConfByte):
        self.conf.stay_awake_when_not_bonded = value
        self.assertEqual(
            self.conf.get_stay_awake_when_not_bonded_byte(),
            expected
        )

    def test_std_and_lp_network(self):
        self.assertTrue(self.conf.std_and_lp_network)
        self.conf.std_and_lp_network = False
        self.assertFalse(self.conf.std_and_lp_network)

    @parameterized.expand([
        [
            False,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=0,
                mask=TrConfBitMasks.STD_AND_LP_NETWORK
            )
        ],
        [
            True,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_0,
                value=128,
                mask=TrConfBitMasks.STD_AND_LP_NETWORK
            )
        ]
    ])
    def test_get_std_and_lp_network_byte(self, value: bool, expected: OsTrConfByte):
        self.conf.std_and_lp_network = value
        self.assertEqual(
            self.conf.get_std_and_lp_network_byte(),
            expected
        )

    def test_rf_output_power(self):
        self.assertEqual(self.conf.rf_output_power, 7)
        self.conf.rf_output_power = 20
        self.assertEqual(self.conf.rf_output_power, 20)

    @parameterized.expand([
        [
            7,
            OsTrConfByte(
                address=TrConfByteAddrs.RF_OUTPUT_POWER,
                value=7,
                mask=0xFF
            )
        ],
        [
            20,
            OsTrConfByte(
                address=TrConfByteAddrs.RF_OUTPUT_POWER,
                value=20,
                mask=0xFF
            )
        ]
    ])
    def test_get_rf_output_power_byte(self, value: int, expected: OsTrConfByte):
        self.conf.rf_output_power = value
        self.assertEqual(
            self.conf.get_rf_output_power_byte(),
            expected
        )

    def test_rf_signal_filter(self):
        self.assertEqual(self.conf.rf_signal_filter, 5)
        self.conf.rf_signal_filter = 10
        self.assertEqual(self.conf.rf_signal_filter, 10)

    @parameterized.expand([
        [
            5,
            OsTrConfByte(
                address=TrConfByteAddrs.RF_SIGNAL_FILTER,
                value=5,
                mask=0xFF
            )
        ],
        [
            10,
            OsTrConfByte(
                address=TrConfByteAddrs.RF_SIGNAL_FILTER,
                value=10,
                mask=0xFF
            )
        ]
    ])
    def test_get_rf_output_power_byte(self, value: int, expected: OsTrConfByte):
        self.conf.rf_signal_filter = value
        self.assertEqual(
            self.conf.get_rf_signal_filter_byte(),
            expected
        )

    def test_lp_rf_timeout(self):
        self.assertEqual(self.conf.lp_rf_timeout, 30)
        self.conf.lp_rf_timeout = 10
        self.assertEqual(self.conf.lp_rf_timeout, 10)

    @parameterized.expand([
        [
            30,
            OsTrConfByte(
                address=TrConfByteAddrs.LP_RF_TIMEOUT,
                value=30,
                mask=0xFF
            )
        ],
        [
            9,
            OsTrConfByte(
                address=TrConfByteAddrs.LP_RF_TIMEOUT,
                value=9,
                mask=0xFF
            )
        ]
    ])
    def test_get_lp_rf_timeout_byte(self, value: int, expected: OsTrConfByte):
        self.conf.lp_rf_timeout = value
        self.assertEqual(
            self.conf.get_lp_rf_timeout_byte(),
            expected
        )

    def test_uart_baud_rate(self):
        self.assertEqual(self.conf.uart_baud_rate, 6)
        self.conf.uart_baud_rate = 1
        self.assertEqual(self.conf.uart_baud_rate, 1)

    @parameterized.expand([
        [
            6,
            OsTrConfByte(
                address=TrConfByteAddrs.UART_BAUD_RATE,
                value=6,
                mask=0xFF
            )
        ],
        [
            1,
            OsTrConfByte(
                address=TrConfByteAddrs.UART_BAUD_RATE,
                value=1,
                mask=0xFF
            )
        ]
    ])
    def test_get_uart_baud_rate_byte(self, value: int, expected: OsTrConfByte):
        self.conf.uart_baud_rate = value
        self.assertEqual(
            self.conf.get_uart_baud_rate_byte(),
            expected
        )

    def test_alternative_dsm_channel(self):
        self.assertEqual(self.conf.alternative_dsm_channel, 20)
        self.conf.alternative_dsm_channel = 2
        self.assertEqual(self.conf.alternative_dsm_channel, 2)

    @parameterized.expand([
        [
            20,
            OsTrConfByte(
                address=TrConfByteAddrs.ALTERNATIVE_DSM_CHANNEL,
                value=20,
                mask=0xFF
            )
        ],
        [
            2,
            OsTrConfByte(
                address=TrConfByteAddrs.ALTERNATIVE_DSM_CHANNEL,
                value=2,
                mask=0xFF
            )
        ]
    ])
    def test_get_alternative_dsm_channel_byte(self, value: int, expected: OsTrConfByte):
        self.conf.alternative_dsm_channel = value
        self.assertEqual(
            self.conf.get_alternative_dsm_channel_byte(),
            expected
        )

    def test_local_frc(self):
        self.assertFalse(self.conf.local_frc)
        self.conf.local_frc = True
        self.assertTrue(self.conf.local_frc)

    @parameterized.expand([
        [
            False,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_1,
                value=0,
                mask=TrConfBitMasks.LOCAL_FRC
            )
        ],
        [
            True,
            OsTrConfByte(
                address=TrConfByteAddrs.DPA_CONFIG_BITS_1,
                value=1,
                mask=TrConfBitMasks.LOCAL_FRC
            )
        ]
    ])
    def test_get_local_frc_byte(self, value: bool, expected: OsTrConfByte):
        self.conf.local_frc = value
        self.assertEqual(
            self.conf.get_local_frc_byte(),
            expected
        )

    def test_rf_channel_a(self):
        self.assertEqual(self.conf.rf_channel_a, 52)
        self.conf.rf_channel_a = 10
        self.assertEqual(self.conf.rf_channel_a, 10)

    @parameterized.expand([
        [
            52,
            OsTrConfByte(
                address=TrConfByteAddrs.RF_CHANNEL_A,
                value=52,
                mask=0xFF
            )
        ],
        [
            10,
            OsTrConfByte(
                address=TrConfByteAddrs.RF_CHANNEL_A,
                value=10,
                mask=0xFF
            )
        ]
    ])
    def test_get_rf_channel_a_byte(self, value: int, expected: OsTrConfByte):
        self.conf.rf_channel_a = value
        self.assertEqual(
            self.conf.get_rf_channel_a_byte(),
            expected
        )

    def test_rf_channel_b(self):
        self.assertEqual(self.conf.rf_channel_b, 1)
        self.conf.rf_channel_b = 17
        self.assertEqual(self.conf.rf_channel_b, 17)

    @parameterized.expand([
        [
            1,
            OsTrConfByte(
                address=TrConfByteAddrs.RF_CHANNEL_B,
                value=1,
                mask=0xFF
            )
        ],
        [
            17,
            OsTrConfByte(
                address=TrConfByteAddrs.RF_CHANNEL_B,
                value=17,
                mask=0xFF
            )
        ]
    ])
    def test_get_rf_channel_b_byte(self, value: int, expected: OsTrConfByte):
        self.conf.rf_channel_b = value
        self.assertEqual(
            self.conf.get_rf_channel_b_byte(),
            expected
        )
