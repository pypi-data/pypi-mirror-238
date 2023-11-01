import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.os.requests.tr_conf_byte import OsTrConfByte


class TrConfByteTest(unittest.TestCase):

    def setUp(self) -> None:
        self.byte = OsTrConfByte(address=8, value=5, mask=255)

    @parameterized.expand([
        [0],
        [25],
        [255]
    ])
    def test_set_address(self, address: int):
        self.byte.address = address
        self.assertEqual(self.byte.address, address)

    @parameterized.expand([
        [-1],
        [256],
        [1000],
    ])
    def test_set_address_invalid(self, address: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            self.byte.address = address

    @parameterized.expand([
        [0],
        [25],
        [255]
    ])
    def test_set_value(self, value: int):
        self.byte.value = value
        self.assertEqual(self.byte.value, value)

    @parameterized.expand([
        [-1],
        [256],
        [1000],
    ])
    def test_set_value_invalid(self, value: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            self.byte.value = value

    @parameterized.expand([
        [0],
        [25],
        [255]
    ])
    def test_set_mask(self, mask: int):
        self.byte.mask = mask
        self.assertEqual(self.byte.mask, mask)

    @parameterized.expand([
        [-1],
        [256],
        [1000],
    ])
    def test_set_mask_invalid(self, mask: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            self.byte.mask = mask

    @parameterized.expand([
        [
            OsTrConfByte(address=17, value=15, mask=128),
            [17, 15, 128],
        ]
    ])
    def test_to_pdata(self, byte: OsTrConfByte, expected: List[int]):
        self.assertEqual(byte.to_pdata(), expected)

    @parameterized.expand([
        [
            OsTrConfByte(address=17, value=15, mask=128),
            {
                'address': 17,
                'value': 15,
                'mask': 128
            },
        ]
    ])
    def test_to_json(self, byte: OsTrConfByte, expected: dict):
        self.assertEqual(byte.to_json(), expected)
