import random
import unittest
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.os.requests.set_security import SetSecurityRequest, OsSecurityType


class SleepRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x02\x06\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.json = {
            'mType': 'iqrfEmbedOs_SetSecurity',
            'data': {
                'msgId': 'setSecurityTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'type': 1,
                        'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [0, [0] * 16, b'\x01\x00\x02\x06\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'],
        [1,
         [1, 2, 3, 4, 5, 10, 7, 12, 255, 0, 0, 0, 1, 14, 2, 8],
         b'\x01\x00\x02\x06\xff\xff\x01\x01\x02\x03\x04\x05\x0a\x07\x0c\xff\x00\x00\x00\x01\x0e\x02\x08'
         ]
    ])
    def test_to_dpa(self, security_type, data, expected):
        request = SetSecurityRequest(nadr=1, security_type=security_type, data=data)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [OsSecurityType.ACCESS_PASSWORD, [0] * 16],
        [OsSecurityType.USER_KEY, [1, 2, 3, 4, 5, 10, 7, 12, 255, 0, 0, 0, 1, 14, 2, 8]]
    ])
    def test_to_json(self, security_type, data):
        request = SetSecurityRequest(nadr=1, security_type=security_type, data=data, msgid='setSecurityTest')
        self.json['data']['req']['param'] = {'type': security_type, 'data': data}
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            OsSecurityType.USER_KEY,
            b'\x01\x00\x02\x06\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ],
        [
            OsSecurityType.ACCESS_PASSWORD,
            b'\x01\x00\x02\x06\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ],
        [
            255,
            b'\x01\x00\x02\x06\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ]
    ])
    def test_set_security_type(self, security_type, dpa):
        request = SetSecurityRequest(nadr=1, security_type=OsSecurityType.USER_KEY, data=[0] * 16, msgid='setSecurityTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.security_type = security_type
        self.json['data']['req']['param']['type'] = security_type
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [[random.randint(0, 255) for _ in range(16)]]
    ])
    def test_set_data(self, data):
        request = SetSecurityRequest(nadr=1, security_type=OsSecurityType.USER_KEY, data=[0] * 16, msgid='setSecurityTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.data = data
        self.json['data']['req']['param']['data'] = data
        self.dpa = self.dpa[0:7] + bytes(data)
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [-1, [random.randint(0, 255) for _ in range(16)]],
        [256, [random.randint(0, 255) for _ in range(16)]],
        [1000, [random.randint(0, 255) for _ in range(16)]],
        [OsSecurityType.ACCESS_PASSWORD, [random.randint(0, 255) for _ in range(5)]],
        [OsSecurityType.USER_KEY, [-1] * 16],
        [5, [256] * 16]
    ])
    def test_invalid_param_members(self, security_type, data):
        with self.assertRaises(RequestParameterInvalidValueError):
            SetSecurityRequest(nadr=1, security_type=security_type, data=data)
