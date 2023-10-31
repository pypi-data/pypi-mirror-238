import unittest
from typing import List, Optional
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.sensor.requests.read_sensors_with_types import ReadSensorsWithTypesRequest
from iqrfpy.peripherals.sensor.requests.sensor_written_data import SensorWrittenData


class ReadSensorsWithTypesRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x5e\x01\xff\xff\x03\x00\x00\x00'
        self.json = {
            'mType': 'iqrfSensor_ReadSensorsWithTypes',
            'data': {
                'msgId': 'readSensorsTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'sensorIndexes': [
                            0,
                            1
                        ]
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [
            'single_pair',
            [SensorWrittenData(index=0, data=[10, 20, 30, 40])],
            b'\x01\x00\x5e\x01\xff\xff\x03\x00\x00\x00\x00\x0a\x14\x1e\x28'
        ],
        [
            'multiple_pairs',
            [
                SensorWrittenData(index=1, data=[0, 1, 2, 3]),
                SensorWrittenData(index=3, data=[5, 7, 8, 9])
            ],
            b'\x01\x00\x5e\x01\xff\xff\x03\x00\x00\x00\x01\x00\x01\x02\x03\x03\x05\x07\x08\x09'
        ]
    ])
    def test_to_dpa(self, _, params, expected):
        request = ReadSensorsWithTypesRequest(nadr=1, sensors=[0, 1], written_data=params)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [
            'single_pair',
            [SensorWrittenData(index=0, data=[10, 20, 30, 40])],
        ],
        [
            'multiple_pairs',
            [
                SensorWrittenData(index=1, data=[0, 1, 2, 3]),
                SensorWrittenData(index=3, data=[5, 7, 8, 9])
            ],
        ]
    ])
    def test_to_json(self, _, params):
        request = ReadSensorsWithTypesRequest(nadr=1, sensors=[0, 1], written_data=params, msgid='readSensorsTest')
        self.json['data']['req']['param']['writtenData'] = [data.to_pdata() for data in params]
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [
            None,
            b'\x01\x00\x5e\x01\xff\xff'
        ],
        [
            [],
            b'\x01\x00\x5e\x01\xff\xff\x00\x00\x00\x00'
        ],
        [
            [0, 1, 2],
            b'\x01\x00\x5e\x01\xff\xff\x07\x00\x00\x00'
        ]
    ])
    def test_set_sensors(self, sensors: Optional[List[int]], dpa: bytes):
        request = ReadSensorsWithTypesRequest(nadr=1, sensors=[0, 1], msgid='readSensorsTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.sensors = sensors
        if sensors is None:
            self.json['data']['req']['param'] = {}
        else:
            self.json['data']['req']['param']['sensorIndexes'] = sensors
        a = request.to_dpa()
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [[-1]],
        [[33]],
        [[0] * 33]
    ])
    def test_set_sensors_invalid(self, sensors: List[int]):
        with self.assertRaises(RequestParameterInvalidValueError):
            ReadSensorsWithTypesRequest(nadr=1, sensors=sensors)

    @parameterized.expand([
        [
            [SensorWrittenData(index=0, data=[10, 20, 30, 40])],
            b'\x01\x00\x5e\x01\xff\xff\x03\x00\x00\x00\x00\x0a\x14\x1e\x28'
        ],
        [
            [
                SensorWrittenData(index=1, data=[0, 1, 2, 3]),
                SensorWrittenData(index=3, data=[5, 7, 8, 9])
            ],
            b'\x01\x00\x5e\x01\xff\xff\x03\x00\x00\x00\x01\x00\x01\x02\x03\x03\x05\x07\x08\x09'
        ]
    ])
    def test_set_written_data(self, written_data: List[SensorWrittenData], dpa):
        request = ReadSensorsWithTypesRequest(nadr=1, sensors=[0, 1], msgid='readSensorsTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.written_data = written_data
        self.json['data']['req']['param']['writtenData'] = [data.to_pdata() for data in written_data]
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [-1, [0, 1, 2, 3]],
        [33, [0, 1, 2, 3]],
        [1, [-1]],
        [1, [256]]
    ])
    def test_set_written_data_invalid(self, index: int, data: List[int]):
        with self.assertRaises(RequestParameterInvalidValueError):
            SensorWrittenData(index=index, data=data)
