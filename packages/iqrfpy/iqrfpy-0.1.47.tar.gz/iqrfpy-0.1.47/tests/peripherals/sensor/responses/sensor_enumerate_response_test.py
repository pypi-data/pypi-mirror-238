import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.enums.commands import SensorResponseCommands
from iqrfpy.enums.message_types import SensorMessages
from iqrfpy.enums.peripherals import Standards
from iqrfpy.exceptions import DpaResponsePacketLengthError
from iqrfpy.peripherals.sensor.responses.enumerate import EnumerateResponse
from iqrfpy.utils.quantity_data import get_sensor_class
from iqrfpy.utils.sensor_parser import SensorTypes, SensorData, SensorParser
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': SensorMessages.ENUMERATE,
    'msgid': 'enumerateTest',
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
                'unit': '°C',
                'decimalPlaces': 4,
                'frcs': [
                     144,
                     224
                ]
            },
            {
                'id': 'BINARYDATA7',
                'type': 129,
                'name': 'Binary data7',
                'shortName': 'bin7',
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
    'dpa': b'\x01\x00\x5e\xbe\x02\x04\x00\x67\x01\x81\x81'
}

data_error: dict = {
    'mtype': SensorMessages.ENUMERATE,
    'msgid': 'enumerateTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x5e\xbe\x04\x04\x01\x23'
}


class EnumerateResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, EnumerateResponse.from_dpa(data_ok['dpa']), False],
        ['from_json', data_ok, EnumerateResponse.from_json(generate_json_response(data_ok)), True],
        ['from_dpa_error', data_error, EnumerateResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, EnumerateResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, Standards.SENSOR)
        with self.subTest():
            self.assertEqual(response.pcmd, SensorResponseCommands.ENUMERATE)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, SensorMessages.ENUMERATE)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(DpaResponsePacketLengthError):
            EnumerateResponse.from_dpa(b'\x01\x00\x5e\xbe\x02')

    @parameterized.expand([
        [
            'from_dpa',
            [
                SensorTypes.TEMPERATURE,
                SensorTypes.BINARY_DATA7,
                SensorTypes.BINARY_DATA7,
            ],
            EnumerateResponse.from_dpa(data_ok['dpa']),
        ],
        [
            'from_json',
            [
                SensorTypes.TEMPERATURE,
                SensorTypes.BINARY_DATA7,
                SensorTypes.BINARY_DATA7,
            ],
            EnumerateResponse.from_json(generate_json_response(data_ok)),
        ],
    ])
    def test_get_sensor_data(self, _, sensors_types: List[int], response: EnumerateResponse):
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
                frc_commands=sensor_class.frc_commands
            )
            sensor_data.append(data)
        self.assertEqual(response.sensor_data, sensor_data)

    @parameterized.expand([
        ['from_dpa_error', EnumerateResponse.from_dpa(data_error['dpa'])],
        ['from_json_error', EnumerateResponse.from_json(generate_json_response(data_error))],
    ])
    def test_get_sensor_data_error(self, _, response: EnumerateResponse):
        self.assertIsNone(response.sensor_data)
