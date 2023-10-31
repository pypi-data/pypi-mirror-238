import unittest
from typing import List

from parameterized import parameterized
from iqrfpy.enums.commands import LEDRequestCommands, OSRequestCommands
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.os.requests.batch import BatchRequest
from iqrfpy.peripherals.os.requests.batch_data import OsBatchData


class BatchRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x02\x05\xff\xff\x05\x06\x01\xff\xff\x00'
        self.json = {
            'mType': 'iqrfEmbedOs_Batch',
            'data': {
                'msgId': 'batchTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
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
            [
                OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON),
            ],
            b'\x01\x00\x02\x05\xff\xff\x05\x06\x01\xff\xff\x00'
        ],
        [
            'two_request_batch',
            [
                OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON),
                OsBatchData(pnum=EmbedPeripherals.OS, pcmd=OSRequestCommands.RESET),
            ],
            b'\x01\x00\x02\x05\xff\xff\x05\x06\x01\xff\xff\x05\x02\x01\xff\xff\x00'
        ]
    ])
    def test_to_dpa(self, _, requests: List[OsBatchData], expected):
        request = BatchRequest(nadr=1, requests=requests)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'single_request_batch',
            [
                OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON),
            ],
        ],
        [
            'two_request_batch',
            [
                OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON),
                OsBatchData(pnum=EmbedPeripherals.OS, pcmd=OSRequestCommands.RESET),
            ],
        ]
    ])
    def test_to_json(self, _, requests: List[OsBatchData]):
        request = BatchRequest(nadr=1, requests=requests, msgid='batchTest')
        self.json['data']['req']['param']['requests'] = [rq.to_json() for rq in requests]
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            [
                OsBatchData(pnum=EmbedPeripherals.OS, pcmd=OSRequestCommands.RESET),
            ],
            b'\x01\x00\x02\x05\xff\xff\x05\x02\x01\xff\xff\x00'
        ],
    ])
    def test_set_requests(self, requests: List[OsBatchData], dpa: bytes):
        default_requests = [OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON)]
        request = BatchRequest(nadr=1, requests=default_requests, msgid='batchTest')
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
            [OsBatchData(pnum=EmbedPeripherals.LEDR, pcmd=LEDRequestCommands.SET_ON)] * 19,
        ],
    ])
    def test_set_too_long(self, requests: List[OsBatchData]):
        with self.assertRaises(RequestParameterInvalidValueError):
            BatchRequest(nadr=1, requests=requests)
