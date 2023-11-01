import unittest
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.os.requests.sleep import SleepRequest, OsSleepParams


class SleepRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x02\x04\xff\xff\x01\x00\x00'
        self.json = {
            'mType': 'iqrfEmbedOs_Sleep',
            'data': {
                'msgId': 'sleepTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'time': 1,
                        'control': 0
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            'no_flags',
            OsSleepParams(time=1),
            b'\x01\x00\x02\x04\xff\xff\x01\x00\x00'
        ],
        [
            'no_time_wake_up_on_edges',
            OsSleepParams(time=0, wake_up_on_negative_edge=True, wake_up_on_positive_edge=True),
            b'\x01\x00\x02\x04\xff\xff\x00\x00\x09'
        ]
    ])
    def test_to_dpa(self, _, params, expected):
        request = SleepRequest(nadr=1, params=params)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'no_flags',
            OsSleepParams(time=1),
            1,
            0
        ],
        [
            'no_time_wake_up_on_edges',
            OsSleepParams(time=0, wake_up_on_negative_edge=True, wake_up_on_positive_edge=True),
            0,
            9
        ]
    ])
    def test_to_json(self, _, params: OsSleepParams, time: int, control: int):
        request = SleepRequest(nadr=1, params=params, msgid='sleepTest')
        self.json['data']['req']['param'] = {'time': time, 'control': control}
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            OsSleepParams(time=0, wake_up_on_negative_edge=True, wake_up_on_positive_edge=True),
            b'\x01\x00\x02\x04\xff\xff\x00\x00\x09'
        ],
    ])
    def test_set_sleep_params(self, params: OsSleepParams, dpa):
        default_params = OsSleepParams(time=1)
        request = SleepRequest(nadr=1, params=default_params, msgid='sleepTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.sleep_params = params
        self.json['data']['req']['param'] = params.to_json()
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
        [65536]
    ])
    def test_invalid_time(self, time: int):
        params = OsSleepParams(time=0)
        with self.assertRaises(RequestParameterInvalidValueError):
            params.time = time
