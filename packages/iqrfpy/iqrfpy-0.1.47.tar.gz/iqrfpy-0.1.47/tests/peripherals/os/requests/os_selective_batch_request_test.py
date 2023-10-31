import random
import unittest
from typing import List

from parameterized import parameterized
from iqrfpy.enums.commands import LEDRequestCommands, OSRequestCommands
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.os.requests.batch_data import OsBatchData
from iqrfpy.peripherals.os.requests.selective_batch import SelectiveBatchRequest


class SelectiveBatchRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\xff\x00\x02\x0b\xff\xff\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x06\x01\xff\xff\x00'
        self.json = {
            'mType': 'iqrfEmbedOs_SelectiveBatch',
            'data': {
                'msgId': 'selectiveBatchTest',
                'req': {
                    'nAdr': 255,
                    'hwpId': 65535,
                    'param': {
                        'selectedNodes': [1, 2, 3],
                        'requests': [
                            {
                                'pnum': '06',
                                'pcmd': '01',
                                'hwpid': 'ffff'
                            }
                        ]
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            'single_request_batch',
            [1, 2, 3],
            [
                OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON),
            ],
            b'\x01\x00\x02\x0b\xff\xff\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x06\x01\xff\xff\x00'
        ],
        [
            'two_request_batch',
            [1, 2, 3],
            [
                OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON),
                OsBatchData(pnum=EmbedPeripherals.OS, pcmd=OSRequestCommands.RESET),
            ],
            b'\x01\x00\x02\x0b\xff\xff\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x06\x01\xff\xff\x05\x02\x01\xff\xff\x00'
        ]
    ])
    def test_to_dpa(self, _, selected_nodes: List[int], requests: List[OsBatchData], expected):
        request = SelectiveBatchRequest(nadr=1, selected_nodes=selected_nodes, requests=requests)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'single_request_batch',
            [1, 2, 3],
            [
                OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON),
            ],
        ],
        [
            'two_request_batch',
            [1, 2, 3],
            [
                OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON),
                OsBatchData(pnum=EmbedPeripherals.OS, pcmd=OSRequestCommands.RESET),
            ],
        ]
    ])
    def test_to_json(self, _, selected_nodes: List[int], requests: List[OsBatchData]):
        request = SelectiveBatchRequest(
            nadr=255,
            selected_nodes=selected_nodes,
            requests=requests,
            msgid='selectiveBatchTest'
        )
        self.json['data']['req']['param'] = {
            'selectedNodes': selected_nodes,
            'requests': [rq.to_json() for rq in requests]
        }
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            [31, 32, 50],
            b'\xff\x00\x02\x0b\xff\xff\x00\x00\x00\x80\x01\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x06\x01\xff\xff\x00'
        ],
        [
            [1, 2, 17, 50, 78],
            b'\xff\x00\x02\x0b\xff\xff\x06\x00\x02\x00\x00\x00\x04\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x06\x01\xff\xff\x00'
        ]
    ])
    def test_set_selected_nodes(self, selected_nodes: List[int], dpa: bytes):
        default_requests = [OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON)]
        request = SelectiveBatchRequest(
            nadr=255,
            selected_nodes=[1, 2, 3],
            requests=default_requests,
            msgid='selectiveBatchTest'
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.selected_nodes = selected_nodes
        self.json['data']['req']['param']['selectedNodes'] = selected_nodes
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [[random.randint(0, 255) for _ in range(250)]],
        [[-1]],
        [[240]],
        [[255]]
    ])
    def test_set_selected_nodes_invalid(self, selected_nodes: List[int]):
        default_requests = [OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON)]
        request = SelectiveBatchRequest(
            nadr=255,
            selected_nodes=[1, 2, 3],
            requests=default_requests,
            msgid='selectiveBatchTest'
        )
        with self.assertRaises(RequestParameterInvalidValueError):
            request.selected_nodes = selected_nodes

    @parameterized.expand([
        [
            [
                OsBatchData(pnum=EmbedPeripherals.OS, pcmd=OSRequestCommands.RESET),
            ],
            b'\xff\x00\x02\x0b\xff\xff\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x02\x01\xff\xff\x00'
        ],
    ])
    def test_set_requests(self, requests: List[OsBatchData], dpa: bytes):
        default_requests = [OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON)]
        request = SelectiveBatchRequest(
            nadr=255,
            selected_nodes=[1, 2, 3],
            requests=default_requests,
            msgid='selectiveBatchTest'
        )
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.requests = requests
        self.json['data']['req']['param']['requests'] = [rq.to_json() for rq in requests]
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            [OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON)] * 7,
        ],
    ])
    def test_set_requests_too_long(self, requests: List[OsBatchData]):
        with self.assertRaises(RequestParameterInvalidValueError):
            SelectiveBatchRequest(nadr=1, selected_nodes=[1, 2, 3], requests=requests)
