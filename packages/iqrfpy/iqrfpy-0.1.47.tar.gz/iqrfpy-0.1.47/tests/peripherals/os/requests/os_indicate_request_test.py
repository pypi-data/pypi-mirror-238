import unittest
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.os.requests.indicate import IndicateRequest, OsIndicateControl


class IndicateRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x02\x07\xff\xff\x03'
        self.json = {
            'mType': 'iqrfEmbedOs_Indicate',
            'data': {
                'msgId': 'indicateTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'control': 3
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            'indicate_off',
            OsIndicateControl.OFF,
            b'\x01\x00\x02\x07\xff\xff\x00',
        ],
        [
            'indicate_on',
            OsIndicateControl.ON,
            b'\x01\x00\x02\x07\xff\xff\x01',
        ],
        [
            'indicate_1s',
            OsIndicateControl.INDICATE_1S,
            b'\x01\x00\x02\x07\xff\xff\x02',
        ],
        [
            'indicate_10s',
            OsIndicateControl.INDICATE_10S,
            b'\x01\x00\x02\x07\xff\xff\x03',
        ],
    ])
    def test_to_dpa(self, _, control: OsIndicateControl, expected: bytes):
        request = IndicateRequest(nadr=1, control=control)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'indicate_off',
            OsIndicateControl.OFF,
        ],
        [
            'indicate_on',
            OsIndicateControl.ON,
        ],
        [
            'indicate_1s',
            OsIndicateControl.INDICATE_1S,
        ],
        [
            'indicate_10s',
            OsIndicateControl.INDICATE_10S,
        ],
    ])
    def test_to_json(self, _, control: OsIndicateControl):
        request = IndicateRequest(nadr=1, control=control, msgid='indicateTest')
        self.json['data']['req']['param']['control'] = control.value
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            OsIndicateControl.ON,
            b'\x01\x00\x02\x07\xff\xff\x01',
        ],
    ])
    def test_set_sleep_params(self, control: OsIndicateControl, dpa: bytes):
        request = IndicateRequest(nadr=1, control=OsIndicateControl.INDICATE_10S, msgid='indicateTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.control = control
        self.json['data']['req']['param']['control'] = control.value
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
