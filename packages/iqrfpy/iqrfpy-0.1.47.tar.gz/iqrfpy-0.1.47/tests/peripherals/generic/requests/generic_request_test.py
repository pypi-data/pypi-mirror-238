import unittest
from parameterized import parameterized
from typing import List, Union, Optional
from iqrfpy.peripherals.generic.requests.generic import GenericRequest
from iqrfpy.enums.commands import Command, CoordinatorRequestCommands, LEDRequestCommands
from iqrfpy.enums.peripherals import Peripheral, EmbedPeripherals


class GenericRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.json = {
            'mType': 'iqrfRaw',
            'data': {
                'msgId': 'test',
                'req': {
                    'rData': '',
                },
                'returnVerbose': True,
            },
        }

    @parameterized.expand([
        [
            'LEDR Pulse enums',
            10,
            EmbedPeripherals.LEDR,
            LEDRequestCommands.PULSE,
            5122,
            None,
            b'\x0a\x00\x06\x03\x02\x14',
        ],
        [
            'LEDR Pulse integers',
            0x0a,
            0x06,
            0x03,
            0x1402,
            None,
            b'\x0a\x00\x06\x03\x02\x14',
        ],
        [
            'Coordinator Bond Node enums',
            0,
            EmbedPeripherals.COORDINATOR,
            CoordinatorRequestCommands.BOND_NODE,
            0,
            [10, 0],
            b'\x00\x00\x00\x04\x00\x00\x0a\x00'
        ],
        [
            'Coordinator Bond Node integers',
            0x00,
            0x00,
            0x04,
            0x0000,
            [0x0a, 0x00],
            b'\x00\x00\x00\x04\x00\x00\x0a\x00'
        ],
    ])
    def test_to_dpa(self, _, nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int], hwpid: int,
                    pdata: Optional[List[int]], expected: bytes):
        request = GenericRequest(nadr=nadr, pnum=pnum, pcmd=pcmd, hwpid=hwpid, pdata=pdata)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'LEDR Pulse enums',
            10,
            EmbedPeripherals.LEDR,
            LEDRequestCommands.PULSE,
            5122,
            None,
            '0a.00.06.03.02.14',
        ],
        [
            'LEDR Pulse integers',
            0x0a,
            0x06,
            0x03,
            0x1402,
            None,
            '0a.00.06.03.02.14',
        ],
        [
            'Coordinator Bond Node enums',
            0,
            EmbedPeripherals.COORDINATOR,
            CoordinatorRequestCommands.BOND_NODE,
            0,
            [10, 0],
            '00.00.00.04.00.00.0a.00',
        ],
        [
            'Coordinator Bond Node integers',
            0x00,
            0x00,
            0x04,
            0x0000,
            [0x0a, 0x00],
            '00.00.00.04.00.00.0a.00',
        ],
    ])
    def test_to_json(self, _, nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int], hwpid: int,
                     pdata: Optional[List[int]], expected: str):
        request = GenericRequest(nadr=nadr, pnum=pnum, pcmd=pcmd, hwpid=hwpid, pdata=pdata, msgid='test')
        self.json['data']['req']['rData'] = expected
        self.assertEqual(
            request.to_json(),
            self.json
        )
