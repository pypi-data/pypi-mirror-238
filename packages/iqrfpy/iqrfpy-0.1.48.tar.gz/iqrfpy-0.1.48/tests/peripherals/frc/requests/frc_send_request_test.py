import random
import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.frc.requests.send import SendRequest


class SendRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x00\x00\x0d\x00\xff\xff\x80\x00\x00'
        self.json = {
            'mType': 'iqrfEmbedFrc_Send',
            'data': {
                'msgId': 'sendTest',
                'req': {
                    'nAdr': 0,
                    'hwpId': 65535,
                    'param': {
                        'frcCommand': 128,
                        'userData': [0, 0]
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        ['ping', 0, [0, 0], b'\x00\x00\x0d\x00\xff\xff\x00\x00\x00'],
        ['temperature', 128, [0, 0], b'\x00\x00\x0d\x00\xff\xff\x80\x00\x00'],
        ['acknowledged_broadcast', 2, [6, 6, 3, 255, 255, 0], b'\x00\x00\x0d\x00\xff\xff\x02\x06\x06\x03\xff\xff\x00']
    ])
    def test_to_dpa(self, _, frc_command: int, user_data: List[int], expected):
        request = SendRequest(nadr=0, frc_command=frc_command, user_data=user_data)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        ['ping', 0, [0, 0]],
        ['temperature', 128, [0, 0]],
        ['acknowledged_broadcast', 2, [6, 6, 3, 255, 255, 0]]
    ])
    def test_to_json(self, _, frc_command: int, user_data: List[int]):
        request = SendRequest(nadr=0, frc_command=frc_command, user_data=user_data, msgid='sendTest')
        self.json['data']['req']['param'] = {'frcCommand': frc_command, 'userData': user_data}
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        ['ping', 0, b'\x00\x00\x0d\x00\xff\xff\x00\x00\x00'],
        ['acknowledged_broadcast', 2, b'\x00\x00\x0d\x00\xff\xff\x02\x00\x00']
    ])
    def test_set_frc_command(self, _, frc_command: int, dpa):
        request = SendRequest(nadr=0, frc_command=128, user_data=[0, 0], msgid='sendTest')
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
        request = SendRequest(nadr=0, frc_command=128, user_data=[0, 0], msgid='sendTest')
        with self.assertRaises(RequestParameterInvalidValueError):
            request.frc_command = frc_command

    @parameterized.expand([
        ['ping', [0, 0], b'\x00\x00\x0d\x00\xff\xff\x80\x00\x00'],
        ['acknowledged_broadcast', [6, 6, 3, 255, 255, 0], b'\x00\x00\x0d\x00\xff\xff\x80\x06\x06\x03\xff\xff\x00']
    ])
    def test_set_user_data(self, _, user_data: List[int], dpa):
        request = SendRequest(nadr=0, frc_command=128, user_data=[0, 0], msgid='sendTest')
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
        [[-1] * 57],
        [[256] * 57]
    ])
    def test_set_user_data_invalid(self, user_data: List[int]):
        request = SendRequest(nadr=0, frc_command=128, user_data=[0, 0], msgid='sendTest')
        with self.assertRaises(RequestParameterInvalidValueError):
            request.user_data = user_data
