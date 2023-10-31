import unittest
from typing import Union
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.frc.requests.set_frc_params import SetFrcParamsRequest, FrcParams
from iqrfpy.utils.dpa import FrcResponseTimes


class SetFrcParamsRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x00\x00\x0d\x03\xff\xff\x00'
        self.json = {
            'mType': 'iqrfEmbedFrc_SetParams',
            'data': {
                'msgId': 'setFrcParamsTest',
                'req': {
                    'nAdr': 0,
                    'hwpId': 65535,
                    'param': {
                        'frcResponseTime': 0
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        ['int_params', 24, b'\x00\x00\x0d\x03\xff\xff\x18'],
        ['class_params',
         FrcParams(offline_frc=True, frc_response_time=FrcResponseTimes.MS360),
         b'\x00\x00\x0d\x03\xff\xff\x18'
         ]
    ])
    def test_to_dpa(self, _, params: Union[FrcParams, int], expected):
        request = SetFrcParamsRequest(nadr=0, frc_params=params)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        ['int_params', 24],
        ['class_params', FrcParams(offline_frc=True, frc_response_time=FrcResponseTimes.MS360)]
    ])
    def test_to_json(self, _, params: Union[FrcParams, int]):
        request = SetFrcParamsRequest(nadr=0, frc_params=params, msgid='setFrcParamsTest')
        self.json['data']['req']['param'] = {'frcResponseTime': params if type(params) == int else params.to_data()}
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        ['int_params', 24, b'\x00\x00\x0d\x03\xff\xff\x18'],
        ['class_params',
         FrcParams(offline_frc=True, frc_response_time=FrcResponseTimes.MS360),
         b'\x00\x00\x0d\x03\xff\xff\x18'
         ]
    ])
    def test_set_frc_params(self, _, params: Union[FrcParams, int], dpa):
        default_params = FrcParams(offline_frc=False, frc_response_time=FrcResponseTimes.MS40)
        request = SetFrcParamsRequest(nadr=0, frc_params=default_params, msgid='setFrcParamsTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.frc_params = params
        self.json['data']['req']['param'] = {'frcResponseTime': params if type(params) == int else params.to_data()}
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
    def test_invalid_params(self, params: int):
        with self.assertRaises(RequestParameterInvalidValueError):
            SetFrcParamsRequest(nadr=0, frc_params=params)
