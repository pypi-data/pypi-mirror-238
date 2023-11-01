import random
import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.io.requests import SetRequest, IoTriplet
from iqrfpy.utils.dpa import IoConstants


class SetRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x09\x01\xff\xff\x00\x04\x04'
        self.json = {
            'mType': 'iqrfEmbedIo_Set',
            'data': {
                'msgId': 'setTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'ports': [
                            {
                                'port': 0,
                                'mask': 4,
                                'value': 4
                            }
                        ]
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            'single_pair',
            [IoTriplet(port=0, mask=255, value=10)],
            b'\x01\x00\x09\x01\xff\xff\x00\xff\x0a'
        ],
        [
            'three_pairs',
            [
                IoTriplet(port=0, mask=255, value=10),
                IoTriplet(port=1, mask=128, value=7),
                IoTriplet(port=17, mask=255, value=255),
            ],
            b'\x01\x00\x09\x01\xff\xff\x00\xff\x0a\x01\x80\x07\x11\xff\xff'
        ]
    ])
    def test_to_dpa(self, _, params: List[IoTriplet], expected: bytes):
        request = SetRequest(nadr=1, triplets=params)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'single_pair',
            [IoTriplet(port=0, mask=255, value=10)],
        ],
        [
            'three_pairs',
            [
                IoTriplet(port=IoConstants.PORT_A, mask=255, value=10),
                IoTriplet(port=1, mask=128, value=7),
                IoTriplet(port=17, mask=255, value=255),
            ],
        ]
    ])
    def test_to_json(self, _, params: List[IoTriplet]):
        request = SetRequest(nadr=1, triplets=params, msgid='setTest')
        self.json['data']['req']['param']['ports'] = [{'port': triplet.port, 'mask': triplet.mask, 'value': triplet.value} for triplet in params]
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            'single_pair',
            [IoTriplet(port=0, mask=255, value=10)],
            b'\x01\x00\x09\x01\xff\xff\x00\xff\x0a'
        ],
        [
            'three_pairs',
            [
                IoTriplet(port=0, mask=255, value=10),
                IoTriplet(port=IoConstants.PORT_B, mask=128, value=7),
                IoTriplet(port=17, mask=255, value=255),
            ],
            b'\x01\x00\x09\x01\xff\xff\x00\xff\x0a\x01\x80\x07\x11\xff\xff'
        ]
    ])
    def test_set_nodes(self, _, params: List[IoTriplet], dpa: bytes):
        nodes = [IoTriplet(port=0, mask=4, value=4)]
        request = SetRequest(nadr=1, triplets=nodes, msgid='setTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.triplets = params
        self.json['data']['req']['param']['ports'] = [{'port': triplet.port, 'mask': triplet.mask, 'value': triplet.value} for triplet in params]
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [-1, 0, 0],
        [256, 0, 0],
        [1000, 5, 5],
        [1, -1, 0],
        [1, 256, 5],
        [1, 1000, 5],
        [1, 5, -1],
        [1, 5, 256],
        [1, 5, 1000]
    ])
    def test_invalid_param_members_constructor(self, port: int, mask: int, value: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            IoTriplet(port=port, mask=mask, value=value)

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_port(self, port: int):
        params = IoTriplet(port=0, mask=4, value=4)
        with self.assertRaises(RequestParameterInvalidValueError):
            params.port = port

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_mask(self, mask: int):
        params = IoTriplet(port=0, mask=4, value=4)
        with self.assertRaises(RequestParameterInvalidValueError):
            params.mask = mask

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_invalid_mask(self, value: int):
        params = IoTriplet(port=0, mask=4, value=4)
        with self.assertRaises(RequestParameterInvalidValueError):
            params.value = value

    @parameterized.expand([
        [[IoTriplet(port=random.randint(0, 255), mask=random.randint(0, 255), value=random.randint(0, 255))] * 19]
    ])
    def test_invalid_pair_count(self, params: List[IoTriplet]):
        with self.assertRaises(RequestParameterInvalidValueError):
            SetRequest(nadr=1, triplets=params)
