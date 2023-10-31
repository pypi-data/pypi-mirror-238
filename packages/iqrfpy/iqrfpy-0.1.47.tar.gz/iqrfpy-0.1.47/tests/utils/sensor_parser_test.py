import unittest
from typing import List, Union
from parameterized import parameterized
from iqrfpy.utils.quantity_data import Temperature, BinaryData7, RelativeHumidity, DataBlock
from iqrfpy.utils.sensor_parser import SensorParser, SensorData
from iqrfpy.utils.sensor_constants import SensorTypes, SensorFrcCommands, SensorFrcErrors


class SensorParserTestCase(unittest.TestCase):

    @parameterized.expand([
        [
            [SensorTypes.TEMPERATURE, SensorTypes.BINARY_DATA7, SensorTypes.BINARY_DATA7],
            [0, 128, 35, 127],
            [
                SensorData(
                    sensor_type=SensorTypes.TEMPERATURE,
                    index=0,
                    name=Temperature.name,
                    short_name=Temperature.short_name,
                    unit=Temperature.unit,
                    decimal_places=Temperature.decimal_places,
                    frc_commands=Temperature.frc_commands,
                    value=None
                ),
                SensorData(
                    sensor_type=SensorTypes.BINARY_DATA7,
                    index=1,
                    name=BinaryData7.name,
                    short_name=BinaryData7.short_name,
                    unit=BinaryData7.unit,
                    decimal_places=BinaryData7.decimal_places,
                    frc_commands=BinaryData7.frc_commands,
                    value=35
                ),
                SensorData(
                    sensor_type=SensorTypes.BINARY_DATA7,
                    index=2,
                    name=BinaryData7.name,
                    short_name=BinaryData7.short_name,
                    unit=BinaryData7.unit,
                    decimal_places=BinaryData7.decimal_places,
                    frc_commands=BinaryData7.frc_commands,
                    value=127
                )
            ]
        ],
        [
            [SensorTypes.RELATIVE_HUMIDITY, SensorTypes.DATA_BLOCK],
            [10, 2, 4, 4],
            [
                SensorData(
                    sensor_type=SensorTypes.RELATIVE_HUMIDITY,
                    index=0,
                    name=RelativeHumidity.name,
                    short_name=RelativeHumidity.short_name,
                    unit=RelativeHumidity.unit,
                    decimal_places=RelativeHumidity.decimal_places,
                    frc_commands=RelativeHumidity.frc_commands,
                    value=5
                ),
                SensorData(
                    sensor_type=SensorTypes.DATA_BLOCK,
                    index=1,
                    name=DataBlock.name,
                    short_name=DataBlock.short_name,
                    unit=DataBlock.unit,
                    decimal_places=DataBlock.decimal_places,
                    frc_commands=DataBlock.frc_commands,
                    value=[4, 4]
                )
            ]
        ]
    ])
    def test_read_sensors_dpa(self, sensor_types: List[SensorTypes], data: List[int], results: List[SensorData]):
        sensor_data = SensorParser.read_sensors_dpa(sensor_types=sensor_types, dpa=data)
        for i in range(len(results)):
            self.assertEqual(sensor_data[i].value, results[i].value)

    @parameterized.expand([
        [
            'unknown_type',
            [30],
            [10]
        ],
        [
            'too_little_sensor_types_for_data',
            [1],
            [10, 20, 30]
        ],
        [
            'too_many_sensor_types_for_data',
            [1, 1, 1],
            [10, 20, 30]
        ],
        [
            'data_block_invalid_data_len',
            [1, 192],
            [10, 20, 5, 10, 20]
        ],
        [
            'data_block_invalid_data_len_2',
            [192],
            [3, 12, 17]
        ]
    ])
    def test_read_sensors_dpa_invalid(self, _, sensor_types: List[SensorTypes], data: List[int]):
        with self.assertRaises(ValueError):
            SensorParser.read_sensors_dpa(sensor_types=sensor_types, dpa=data)

    @parameterized.expand([
        [
            '2bit_frc_bin7_no_count',
            SensorTypes.BINARY_DATA7,
            33,
            SensorFrcCommands.FRC_2BITS,
            [14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            None,
            [1, SensorFrcErrors.FRC_NOT_IMPLEMENTED, 1] + [SensorFrcErrors.NO_FRC_RESPONSE] * 236
        ],
        [
            '2bit_bin7_count',
            SensorTypes.BINARY_DATA7,
            33,
            SensorFrcCommands.FRC_2BITS,
            [14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            3,
            [1, SensorFrcErrors.FRC_NOT_IMPLEMENTED, 1]
        ],
        [
            '1byte_temperature_no_count',
            SensorTypes.TEMPERATURE,
            0,
            SensorFrcCommands.FRC_1BYTE,
            [0, 2, 104, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            None,
            [SensorFrcErrors.SENSOR_ERROR_OR_OUT_OF_RANGE, 30, SensorFrcErrors.SENSOR_ERROR_OR_OUT_OF_RANGE] + [
                SensorFrcErrors.NO_FRC_RESPONSE] * 60
        ],
        [
            '1byte_temperature_count',
            SensorTypes.TEMPERATURE,
            0,
            SensorFrcCommands.FRC_1BYTE,
            [0, 2, 104, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            5,
            [SensorFrcErrors.SENSOR_ERROR_OR_OUT_OF_RANGE, 30, SensorFrcErrors.SENSOR_ERROR_OR_OUT_OF_RANGE] + [
                SensorFrcErrors.NO_FRC_RESPONSE] * 2
        ],
        [
            '2byte_temperature_no_count',
            SensorTypes.TEMPERATURE,
            0,
            SensorFrcCommands.FRC_2BYTES,
            [0, 0, 2, 0, 216, 129, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            None,
            [SensorFrcErrors.SENSOR_ERROR_OR_OUT_OF_RANGE, 29.5, SensorFrcErrors.SENSOR_ERROR_OR_OUT_OF_RANGE] + [
                SensorFrcErrors.NO_FRC_RESPONSE] * 28
        ],
        [
            '2byte_temperature_count',
            SensorTypes.TEMPERATURE,
            0,
            SensorFrcCommands.FRC_2BYTES,
            [0, 0, 2, 0, 216, 129, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            4,
            [SensorFrcErrors.SENSOR_ERROR_OR_OUT_OF_RANGE, 29.5, SensorFrcErrors.SENSOR_ERROR_OR_OUT_OF_RANGE] + [
                SensorFrcErrors.NO_FRC_RESPONSE] * 1
        ],
        [
            '4byte_bin30_no_count',
            SensorTypes.BINARY_DATA30,
            0,
            SensorFrcCommands.FRC_4BYTES,
            [0, 0, 0, 0, 1, 0, 0, 0, 40, 124, 17, 129, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            None,
            [SensorFrcErrors.FRC_NOT_IMPLEMENTED, 2165406756, SensorFrcErrors.FRC_NOT_IMPLEMENTED] + [
                SensorFrcErrors.NO_FRC_RESPONSE] * 12
        ],
        [
            '4byte_bin30_count',
            SensorTypes.BINARY_DATA30,
            0,
            SensorFrcCommands.FRC_4BYTES,
            [0, 0, 0, 0, 1, 0, 0, 0, 40, 124, 17, 129, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            6,
            [SensorFrcErrors.FRC_NOT_IMPLEMENTED, 2165406756, SensorFrcErrors.FRC_NOT_IMPLEMENTED] + [
                SensorFrcErrors.NO_FRC_RESPONSE] * 3
        ]
    ])
    def test_frc_data(self, _, sensor_type: int, sensor_index: int, frc_command: int, frc_data: List[int],
                      extra_result: List[int], count: Union[int, None],
                      values: List[Union[int, float, List[int], SensorFrcErrors]]
                      ):
        sensor_data = SensorParser.frc_dpa(
            sensor_type=sensor_type,
            sensor_index=sensor_index,
            frc_command=frc_command,
            data=frc_data,
            extra_result=extra_result,
            count=count
        )
        for i in range(len(values)):
            self.assertEqual(sensor_data[i].value, values[i])

    @parameterized.expand([
        [
            'unknown_sensor',
            30,
            0,
            SensorFrcCommands.FRC_1BYTE,
            [],
            [],
            None
        ],
        [
            '2bit_too_short',
            129,
            0,
            SensorFrcCommands.FRC_2BITS,
            [],
            [],
            None
        ],
        [
            '2byte_invalid_len_no_count',
            1,
            0,
            SensorFrcCommands.FRC_2BYTES,
            [0] * 55,
            [],
            None
        ],
        [
            '2byte_invalid_len_count',
            1,
            0,
            SensorFrcCommands.FRC_2BYTES,
            [0] * 5,
            [],
            10
        ],
        [
            '4byte_invalid_len_no_count',
            160,
            0,
            SensorFrcCommands.FRC_4BYTES,
            [0] * 55,
            [],
            None
        ],
        [
            '4byte_invalid_len_count',
            160,
            0,
            SensorFrcCommands.FRC_4BYTES,
            [0] * 10,
            [0],
            3
        ]
    ])
    def test_frc_data_invalid(self, _, sensor_type: int, sensor_index: int, frc_command: int, frc_data: List[int],
                              extra_result: List[int], count: Union[int, None]):
        with self.assertRaises(ValueError):
            SensorParser.frc_dpa(
                sensor_type=sensor_type,
                sensor_index=sensor_index,
                frc_command=frc_command,
                data=frc_data,
                extra_result=extra_result,
                count=count
            )
