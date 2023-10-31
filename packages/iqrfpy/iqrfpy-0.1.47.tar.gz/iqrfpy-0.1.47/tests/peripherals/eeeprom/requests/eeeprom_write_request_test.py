import random
import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.eeeprom.requests.write import WriteRequest


class WriteRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x05\x00\x04\x03\xff\xff\x0a\x00\x00\x01\x02\x03\x04'
        self.json = {
            'mType': 'iqrfEmbedEeeprom_Write',
            'data': {
                'msgId': 'writeTest',
                'req': {
                    'nAdr': 5,
                    'hwpId': 65535,
                    'param': {
                        'address': 10,
                        'pData': [0, 1, 2, 3, 4]
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [5, 10, [2, 7, 2, 1, 3], b'\x05\x00\x04\x03\xff\xff\x0a\x00\x02\x07\x02\x01\x03'],
        [0, 5, [12, 17, 0, 255, 7], b'\x00\x00\x04\x03\xff\xff\x05\x00\x0c\x11\x00\xff\x07'],
    ])
    def test_to_dpa(self, nadr: int, address: int, data: List[int], expected):
        request = WriteRequest(nadr=nadr, address=address, data=data)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [5, 10, [2, 7, 2, 1, 3]],
        [0, 5, [12, 17, 0, 255, 7]],
    ])
    def test_to_json(self, nadr: int, address: int, data: List[int]):
        request = WriteRequest(nadr=nadr, address=address, data=data, msgid='writeTest')
        self.json['data']['req']['nAdr'] = nadr
        self.json['data']['req']['param']['address'] = address
        self.json['data']['req']['param']['pData'] = data
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [2, b'\x05\x00\x04\x03\xff\xff\x02\x00\x00\x01\x02\x03\x04'],
        [17, b'\x05\x00\x04\x03\xff\xff\x11\x00\x00\x01\x02\x03\x04'],
    ])
    def test_set_address(self, address: int, dpa: bytes):
        request = WriteRequest(nadr=5, address=10, data=[0, 1, 2, 3, 4], msgid='writeTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.address = address
        self.json['data']['req']['param']['address'] = address
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
        [65536],
        [100000]
    ])
    def test_set_address_invalid(self, address):
        request = WriteRequest(nadr=5, address=10, data=[0, 1, 2, 3, 4], msgid='writeTest')
        with self.assertRaises(RequestParameterInvalidValueError):
            request.address = address

    @parameterized.expand([
        [[12, 17, 0, 255, 7], b'\x05\x00\x04\x03\xff\xff\x0a\x00\x0c\x11\x00\xff\x07'],
        [[2, 7, 2, 1, 3], b'\x05\x00\x04\x03\xff\xff\x0a\x00\x02\x07\x02\x01\x03'],
    ])
    def test_set_data(self, data: List[int], dpa):
        request = WriteRequest(nadr=5, address=10, data=[0, 1, 2, 3, 4], msgid='writeTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.data = data
        self.json['data']['req']['param']['pData'] = data
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [[random.randint(0, 255)] * 60],
        [[10, 20, 75, 255, 1000]]
    ])
    def test_set_data_invalid(self, data: List[int]):
        request = WriteRequest(nadr=5, address=10, data=[0, 1, 2, 3, 4], msgid='writeTest')
        with self.assertRaises(RequestParameterInvalidValueError):
            request.data = data

    @parameterized.expand([
        [-1, [1]],
        [65536, [10]],
        [100000, [15]],
        [10, [random.randint(0, 255)] * 60],
        [10, [10, 20, 75, 255, 1000]]
    ])
    def test_construct_invalid(self, address: int, data: List[int]):
        with self.assertRaises(RequestParameterInvalidValueError):
            WriteRequest(nadr=0, address=address, data=data)
