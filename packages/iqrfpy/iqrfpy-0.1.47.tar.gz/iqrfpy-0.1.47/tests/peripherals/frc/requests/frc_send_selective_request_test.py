import random
import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.frc.requests.send_selective import SendSelectiveRequest


class SendSelectiveRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x00\x00\x0d\x02\xff\xff\x80\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                   b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.json = {
            'mType': 'iqrfEmbedFrc_SendSelective',
            'data': {
                'msgId': 'sendSelectiveTest',
                'req': {
                    'nAdr': 0,
                    'hwpId': 65535,
                    'param': {
                        'frcCommand': 128,
                        'selectedNodes': [1, 2, 3],
                        'userData': [0, 0]
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            'ping',
            0,
            [1, 2, 3],
            [0, 0],
            b'\x00\x00\x0d\x02\xff\xff\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ],
        [
            'temperature',
            128,
            [1, 2, 3],
            [0, 0],
            b'\x00\x00\x0d\x02\xff\xff\x80\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ],
        [
            'acknowledged_broadcast',
            2,
            [1, 2, 3],
            [6, 6, 3, 255, 255, 0],
            b'\x00\x00\x0d\x02\xff\xff\x02\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x06\x03\xff\xff\x00'
        ]
    ])
    def test_to_dpa(self, _, frc_command: int, selected_nodes: List[int], user_data: List[int], expected):
        request = SendSelectiveRequest(nadr=0, frc_command=frc_command, selected_nodes=selected_nodes,
                                       user_data=user_data)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        ['ping', 0, [1, 2, 3], [0, 0]],
        ['temperature', 128, [1, 2, 3], [0, 0]],
        ['acknowledged_broadcast', 2, [1, 2, 3], [6, 6, 3, 255, 255, 0]]
    ])
    def test_to_json(self, _, frc_command: int, selected_nodes: List[int], user_data: List[int]):
        request = SendSelectiveRequest(nadr=0, frc_command=frc_command, selected_nodes=selected_nodes,
                                       user_data=user_data, msgid='sendSelectiveTest')
        self.json['data']['req']['param'] = {
            'frcCommand': frc_command,
            'selectedNodes': selected_nodes,
            'userData': user_data
        }
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            'ping',
            0,
            b'\x00\x00\x0d\x02\xff\xff\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ],
        [
            'acknowledged_broadcast',
            2,
            b'\x00\x00\x0d\x02\xff\xff\x02\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ]
    ])
    def test_set_frc_command(self, _, frc_command: int, dpa):
        request = SendSelectiveRequest(nadr=0, frc_command=128, selected_nodes=[1, 2, 3], user_data=[0, 0],
                                       msgid='sendSelectiveTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.frc_command = frc_command
        self.json['data']['req']['param']['frcCommand'] = frc_command
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_set_frc_command_invalid(self, frc_command: int):
        request = SendSelectiveRequest(nadr=0, frc_command=128, selected_nodes=[1, 2, 3], user_data=[0, 0],
                                       msgid='sendSelectiveTest')
        with self.assertRaises(RequestParameterInvalidValueError):
            request.frc_command = frc_command

    @parameterized.expand([
        [
            [31, 32, 50],
            b'\x00\x00\x0d\x02\xff\xff\x80\x00\x00\x00\x80\x01\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ],
        [
            [1, 2, 17, 50, 78],
            b'\x00\x00\x0d\x02\xff\xff\x80\x06\x00\x02\x00\x00\x00\x04\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ]
    ])
    def test_set_selected_nodes(self, selected_nodes: List[int], dpa):
        request = SendSelectiveRequest(nadr=0, frc_command=128, selected_nodes=[1, 2, 3], user_data=[0, 0],
                                       msgid='sendSelectiveTest')
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
        request = SendSelectiveRequest(nadr=0, frc_command=128, selected_nodes=[1, 2, 3], user_data=[0, 0],
                                       msgid='sendSelectiveTest')
        with self.assertRaises(RequestParameterInvalidValueError):
            request.selected_nodes = selected_nodes

    @parameterized.expand([
        [
            'ping',
            [0, 0],
            b'\x00\x00\x0d\x02\xff\xff\x80\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ],
        [
            'acknowledged_broadcast',
            [6, 6, 3, 255, 255, 0],
            b'\x00\x00\x0d\x02\xff\xff\x80\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x06\x03\xff\xff\x00'
        ]
    ])
    def test_set_user_data(self, _, user_data: List[int], dpa):
        request = SendSelectiveRequest(nadr=0, frc_command=128, selected_nodes=[1, 2, 3], user_data=[0, 0],
                                       msgid='sendSelectiveTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.user_data = user_data
        self.json['data']['req']['param']['userData'] = user_data
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [[random.randint(0, 255) for _ in range(60)]],
        [[-1] * 27],
        [[256] * 27]
    ])
    def test_set_user_data_invalid(self, user_data: List[int]):
        request = SendSelectiveRequest(nadr=0, frc_command=128, selected_nodes=[1, 2, 3], user_data=[0, 0],
                                       msgid='sendSelectiveTest')
        with self.assertRaises(RequestParameterInvalidValueError):
            request.user_data = user_data
