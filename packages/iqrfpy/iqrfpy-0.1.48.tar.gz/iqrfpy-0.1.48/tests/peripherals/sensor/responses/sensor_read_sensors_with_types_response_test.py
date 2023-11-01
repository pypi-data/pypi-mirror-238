import unittest
from typing import List, Union
from parameterized import parameterized
from iqrfpy.enums.commands import SensorResponseCommands
from iqrfpy.enums.message_types import SensorMessages
from iqrfpy.enums.peripherals import Standards
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.sensor.responses.read_sensors_with_types import ReadSensorsWithTypesResponse
from iqrfpy.utils.quantity_data import get_sensor_class
from iqrfpy.utils.sensor_parser import SensorTypes, SensorData
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': SensorMessages.READ_SENSORS_WITH_TYPES,
    'msgid': 'readSensorsTest',
    'nadr': 1,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 103,
    'result': {
        'sensors': [
            {
                'id': 'TEMPERATURE',
                'type': 1,
                'name': 'Temperature',
                'shortName': 't',
                'value': None,
                'unit': '°C',
                'decimalPlaces': 4,
                'frcs': [
                     144,
                     224
                ],
            },
            {
                'id': 'BINARYDATA7',
                'type': 129,
                'name': 'Binary data7',
                'shortName': 'bin7',
                'value': 35,
                'unit': '?',
                'decimalPlaces': 0,
                'frcs': [
                     16,
                     144
                ],
                'breakdown': [
                     {
                        'id': 'BINARYDATA7',
                        'type': 129,
                        'name': 'Light indicator',
                        'shortName': 'light',
                        'unit': '%',
                        'decimalPlaces': 1
                     }
                ]
            },
            {
                'id': 'BINARYDATA7',
                'type': 129,
                'name': 'Binary data7',
                'shortName': 'bin7',
                'value': 127,
                'unit': '?',
                'decimalPlaces': 0,
                'frcs': [
                     16,
                     144
                ],
                'breakdown': [
                     {
                        'id': 'BINARYDATA7',
                        'type': 129,
                        'name': 'Potentiometer',
                        'shortName': 'pot',
                        'unit': '%',
                        'decimalPlaces': 1
                     }
                ]
            }
        ]
    },
    'dpa': b'\x01\x00\x5e\x81\x02\x04\x00\x67\x01\x00\x80\x81\x23\x81\x7f'
}

data_error: dict = {
    'mtype': SensorMessages.READ_SENSORS_WITH_TYPES,
    'msgid': 'readSensorsTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x5e\x81\x04\x04\x01\x23'
}


class ReadSensorsWithTypesTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, ReadSensorsWithTypesResponse.from_dpa(data_ok['dpa']), False],
        ['from_json', data_ok, ReadSensorsWithTypesResponse.from_json(generate_json_response(data_ok)), True],
        ['from_dpa_error', data_error, ReadSensorsWithTypesResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, ReadSensorsWithTypesResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, Standards.SENSOR)
        with self.subTest():
            self.assertEqual(response.pcmd, SensorResponseCommands.READ_SENSORS_WITH_TYPES)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, SensorMessages.READ_SENSORS_WITH_TYPES)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            ReadSensorsWithTypesResponse.from_dpa(b'\x01\x00\x5e\xbe\x02')

    @parameterized.expand([
        [
            'from_dpa',
            [
                SensorTypes.TEMPERATURE,
                SensorTypes.BINARY_DATA7,
                SensorTypes.BINARY_DATA7,
            ],
            [None, 35, 127],
            ReadSensorsWithTypesResponse.from_dpa(data_ok['dpa']),
        ],
        [
            'from_json',
            [
                SensorTypes.TEMPERATURE,
                SensorTypes.BINARY_DATA7,
                SensorTypes.BINARY_DATA7,
            ],
            [None, 35, 127],
            ReadSensorsWithTypesResponse.from_json(generate_json_response(data_ok)),
        ],
    ])
    def test_get_sensor_data(self, _, sensors_types: List[SensorTypes], values: List[Union[int, float, None]],
                             response: ReadSensorsWithTypesResponse):
        sensor_data = []
        for i in sensors_types:
            sensor_class = get_sensor_class(i)
            data = SensorData(
                sensor_type=sensor_class.type,
                index=len(sensor_data),
                name=sensor_class.name,
                short_name=sensor_class.short_name,
                unit=sensor_class.unit,
                decimal_places=sensor_class.decimal_places,
                frc_commands=sensor_class.frc_commands,
                value=values[len(sensor_data)]
            )
            sensor_data.append(data)
        self.assertEqual(response.sensor_data, sensor_data)

    @parameterized.expand([
        ['from_dpa_error', ReadSensorsWithTypesResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', ReadSensorsWithTypesResponse.from_json(generate_json_response(data_error))],
    ])
    def test_get_sensor_data_error(self, _, response: ReadSensorsWithTypesResponse):
        self.assertIsNone(response.sensor_data)
