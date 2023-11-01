import random
import unittest
from parameterized import parameterized
from typing import List
from iqrfpy.enums.message_types import BinaryOutputMessages
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.binaryoutput.requests.binary_output_state import BinaryOutputState
from iqrfpy.peripherals.binaryoutput.requests.set_output import SetOutputRequest


class SetOutputRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x03\x00\x4b\x00\xff\xff\x00\x00\x00\x00'
        self.json = {
            'mType': BinaryOutputMessages.SET_OUTPUT.value,
            'data': {
                'msgId': 'setOutputTest',
                'req': {
                    'nAdr': 3,
                    'hwpId': 65535,
                    'param': {
                        'binOuts': [],
                    },
                },
                'returnVerbose': True,
            },
        }

    @parameterized.expand([
        [
            'single_pair',
            [
                BinaryOutputState(index=0, state=10)
            ],
            b'\x03\x00\x4b\x00\xff\xff\x01\x00\x00\x00\x0a'
        ],
        [
            'three_pairs',
            [
                BinaryOutputState(index=10, state=30),
                BinaryOutputState(index=5, state=10),
                BinaryOutputState(index=1, state=255)
            ],
            b'\x03\x00\x4b\x00\xff\xff\x22\x04\x00\x00\xff\x0a\x1e'
        ],
    ])
    def test_to_dpa(self, _, binouts: List[BinaryOutputState], expected: bytes):
        request = SetOutputRequest(nadr=3, binouts=binouts)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'single_pair',
            [
                BinaryOutputState(index=0, state=10)
            ],
        ],
        [
            'three_pairs',
            [
                BinaryOutputState(index=10, state=30),
                BinaryOutputState(index=5, state=10),
                BinaryOutputState(index=1, state=255)
            ],
        ],
    ])
    def test_to_json(self, _, binouts: List[BinaryOutputState]):
        request = SetOutputRequest(nadr=3, msgid='setOutputTest')
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.binouts = binouts
        self.json['data']['req']['param']['binOuts'] = [bo.to_json() for bo in binouts]
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            'single_pair',
            [
                BinaryOutputState(index=0, state=10)
            ],
            b'\x03\x00\x4b\x00\xff\xff\x01\x00\x00\x00\x0a'
        ],
        [
            'three_pairs',
            [
                BinaryOutputState(index=10, state=30),
                BinaryOutputState(index=5, state=10),
                BinaryOutputState(index=1, state=255)
            ],
            b'\x03\x00\x4b\x00\xff\xff\x22\x04\x00\x00\xff\x0a\x1e'
        ],
    ])
    def test_set_binouts(self, _, binouts: List[BinaryOutputState], dpa: bytes):
        request = SetOutputRequest(nadr=3, msgid='setOutputTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.binouts = binouts
        self.json['data']['req']['param']['binOuts'] = [bo.to_json() for bo in binouts]
        self.assertEqual(
            request.binouts,
            binouts
        )
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [-1, 0],
        [255, 0],
        [32, 0],
        [1, -1],
        [1, 256],
        [1, 1000],
    ])
    def test_invalid_binary_output_state_member_constructor(self, index: int, state: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            BinaryOutputState(index=index, state=state)

    @parameterized.expand([
        [-1],
        [32],
        [255],
    ])
    def test_invalid_binary_output_index(self, index: int):
        bo_state = BinaryOutputState(index=0, state=1)
        with self.assertRaises(RequestParameterInvalidValueError):
            bo_state.index = index

    @parameterized.expand([
        [-1],
        [256],
        [1000],
    ])
    def test_invalid_binary_output_state(self, state: int):
        bo_state = BinaryOutputState(index=0, state=1)
        with self.assertRaises(RequestParameterInvalidValueError):
            bo_state.state = state

    @parameterized.expand([
        [
            [
                BinaryOutputState(
                    index=random.randint(0, 31),
                    state=random.randint(0, 255),
                )
                for _ in range(33)
            ]
        ]
    ])
    def test_invalid_state_count(self, binouts: List[BinaryOutputState]):
        with self.assertRaises(RequestParameterInvalidValueError):
            SetOutputRequest(nadr=3, binouts=binouts)
