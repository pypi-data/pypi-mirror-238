import unittest
from typing import List, Optional
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.sensor.requests.read_sensors import ReadSensorsRequest
from iqrfpy.peripherals.sensor.requests.sensor_written_data import SensorWrittenData


class ReadSensorsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x5e\x00\xff\xff\x03\x00\x00\x00'

    @parameterized.expand([
        [
            'single_pair',
            [SensorWrittenData(index=0, data=[10, 20, 30, 40])],
            b'\x01\x00\x5e\x00\xff\xff\x03\x00\x00\x00\x00\x0a\x14\x1e\x28'
        ],
        [
            'multiple_pairs',
            [
                SensorWrittenData(index=1, data=[0, 1, 2, 3]),
                SensorWrittenData(index=3, data=[5, 7, 8, 9])
            ],
            b'\x01\x00\x5e\x00\xff\xff\x03\x00\x00\x00\x01\x00\x01\x02\x03\x03\x05\x07\x08\x09'
        ]
    ])
    def test_to_dpa(self, _, params, expected):
        request = ReadSensorsRequest(nadr=1, sensors=[0, 1], written_data=params)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    def test_to_json(self):
        request = ReadSensorsRequest(nadr=1, sensors=[0, 1], msgid='readSensorsTest')
        with self.assertRaises(NotImplementedError):
            request.to_json()

    @parameterized.expand([
        [
            None,
            b'\x01\x00\x5e\x00\xff\xff'
        ],
        [
            [],
            b'\x01\x00\x5e\x00\xff\xff\x00\x00\x00\x00'
        ],
        [
            [0, 1, 2],
            b'\x01\x00\x5e\x00\xff\xff\x07\x00\x00\x00'
        ]
    ])
    def test_set_sensors(self, sensors: Optional[List[int]], dpa: bytes):
        request = ReadSensorsRequest(nadr=1, sensors=[0, 1], msgid='readSensorsTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        request.sensors = sensors
        self.assertEqual(
            request.to_dpa(),
            dpa
        )

    @parameterized.expand([
        [[-1]],
        [[33]],
        [[0] * 33]
    ])
    def test_set_sensors_invalid(self, sensors: List[int]):
        with self.assertRaises(RequestParameterInvalidValueError):
            ReadSensorsRequest(nadr=1, sensors=sensors)

    @parameterized.expand([
        [
            [SensorWrittenData(index=0, data=[10, 20, 30, 40])],
            b'\x01\x00\x5e\x00\xff\xff\x03\x00\x00\x00\x00\x0a\x14\x1e\x28'
        ],
        [
            [
                SensorWrittenData(index=1, data=[0, 1, 2, 3]),
                SensorWrittenData(index=3, data=[5, 7, 8, 9])
            ],
            b'\x01\x00\x5e\x00\xff\xff\x03\x00\x00\x00\x01\x00\x01\x02\x03\x03\x05\x07\x08\x09'
        ]
    ])
    def test_set_written_data(self, written_data: List[SensorWrittenData], dpa):
        request = ReadSensorsRequest(nadr=1, sensors=[0, 1], msgid='readSensorsTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        request.written_data = written_data
        self.assertEqual(
            request.to_dpa(),
            dpa
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
