import random
import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.os.requests.tr_conf_byte import OsTrConfByte
from iqrfpy.peripherals.os.requests.write_tr_conf_byte import WriteTrConfByteRequest


class WriteTrConfByteRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x02\x09\xff\xff\x08\x05\xff'
        self.json = {
            'mType': 'iqrfEmbedOs_WriteCfgByte',
            'data': {
                'msgId': 'writeTrConfByteTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'bytes': [
                            {
                                'address': 8,
                                'value': 5,
                                'mask': 255
                            }
                        ]
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            [
                OsTrConfByte(address=12, value=10, mask=10),
                OsTrConfByte(address=5, value=8, mask=255),
            ],
            b'\x01\x00\x02\x09\xff\xff\x0c\x0a\x0a\x05\x08\xff'
        ]
    ])
    def test_to_dpa(self, configuration_bytes: List[OsTrConfByte], expected: bytes):
        request = WriteTrConfByteRequest(nadr=1, configuration_bytes=configuration_bytes)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            [
                OsTrConfByte(address=12, value=10, mask=10),
                OsTrConfByte(address=5, value=8, mask=255),
            ],
        ]
    ])
    def test_to_json(self, configuration_bytes: List[OsTrConfByte]):
        request = WriteTrConfByteRequest(nadr=1, configuration_bytes=configuration_bytes, msgid='writeTrConfByteTest')
        self.json['data']['req']['param']['bytes'] = [byte.to_json() for byte in configuration_bytes]
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            [
                OsTrConfByte(address=12, value=10, mask=10),
                OsTrConfByte(address=5, value=8, mask=255),
            ],
            b'\x01\x00\x02\x09\xff\xff\x0c\x0a\x0a\x05\x08\xff'
        ]
    ])
    def test_set_configuration_bytes(self, configuration_bytes: List[OsTrConfByte], dpa: bytes):
        default_bytes = [OsTrConfByte(address=8, value=5, mask=255)]
        request = WriteTrConfByteRequest(nadr=1, configuration_bytes=default_bytes, msgid='writeTrConfByteTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.configuration_bytes = configuration_bytes
        self.json['data']['req']['param']['bytes'] = [byte.to_json() for byte in configuration_bytes]
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
            [
                OsTrConfByte(
                    address=random.randint(0, 255),
                    value=random.randint(0, 255),
                    mask=random.randint(0, 255)
                ) for _ in range(19)
            ]
        ]
    ])
    def test_set_configuration_bytes_invalid(self, configuration_bytes: List[OsTrConfByte]):
        default_bytes = [OsTrConfByte(address=8, value=5, mask=255)]
        request = WriteTrConfByteRequest(nadr=1, configuration_bytes=default_bytes, msgid='writeTrConfByteTest')
        with self.assertRaises(RequestParameterInvalidValueError):
            request.configuration_bytes = configuration_bytes
