import random
import unittest
from typing import List, Union
from parameterized import parameterized

from iqrfpy.enums.commands import Command, CoordinatorRequestCommands, LEDRequestCommands
from iqrfpy.enums.peripherals import Peripheral, EmbedPeripherals, Standards
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.os.requests.batch_data import OsBatchData


class BatchDataTest(unittest.TestCase):

    def setUp(self) -> None:
        self.data = OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON)

    @parameterized.expand([
        [EmbedPeripherals.OS],
        [EmbedPeripherals.EEPROM],
        [Standards.SENSOR],
        [0],
        [13],
        [70],
    ])
    def test_set_pnum(self, pnum: Union[Peripheral, int]):
        self.data.pnum = pnum
        self.assertEqual(self.data.pnum, pnum)

    @parameterized.expand([
        [-1],
        [256],
        [1000],
    ])
    def test_set_pnum_invalid(self, pnum: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            self.data.pnum = pnum

    @parameterized.expand([
        [LEDRequestCommands.SET_OFF],
        [LEDRequestCommands.SET_ON],
        [3],
        [13],
        [70],
    ])
    def test_set_pcmd(self, pcmd: Union[Command, int]):
        self.data.pcmd = pcmd
        self.assertEqual(self.data.pcmd, pcmd)

    @parameterized.expand([
        [-1],
        [256],
        [1000],
    ])
    def test_set_pcmd_invalid(self, pcmd: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            self.data.pcmd = pcmd

    @parameterized.expand([
        [0],
        [256],
        [1000],
        [65535],
    ])
    def test_set_hwpid(self, hwpid: int):
        self.data.hwpid = hwpid
        self.assertEqual(self.data.hwpid, hwpid)

    @parameterized.expand([
        [-1],
        [65536],
        [100000],
    ])
    def test_set_hwpid_invalid(self, hwpid: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            self.data.hwpid = hwpid

    @parameterized.expand([
        [
            [random.randint(0, 255)] * 58,
        ],
    ])
    def test_set_pdata(self, pdata: List[int]):
        self.data.pdata = pdata
        self.assertEqual(self.data.pdata, pdata)

    @parameterized.expand([
        [
            [-1],
        ],
        [
            [5, 6, 7, 8, 9, 1520],
        ],
    ])
    def test_set_pdata_invalid(self, pdata: List[int]):
        with self.assertRaises(RequestParameterInvalidValueError):
            self.data.pdata = pdata

    @parameterized.expand([
        [
            OsBatchData(pnum=EmbedPeripherals.COORDINATOR, pcmd=CoordinatorRequestCommands.BOND_NODE, pdata=[1, 1]),
            [7, 0, 4, 255, 255, 1, 1],
        ]
    ])
    def test_to_dpa(self, request: OsBatchData, expected: List[int]):
        self.assertEqual(request.to_pdata(), expected)

    @parameterized.expand([
        [
            OsBatchData(pnum=EmbedPeripherals.COORDINATOR, pcmd=CoordinatorRequestCommands.BOND_NODE, pdata=[1, 1]),
            {
                'pnum': '00',
                'pcmd': '04',
                'hwpid': 'ffff',
                'rdata': '01.01',
            },
        ]
    ])
    def test_to_json(self, request: OsBatchData, expected: dict):
        self.assertEqual(request.to_json(), expected)
