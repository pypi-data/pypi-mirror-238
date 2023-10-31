import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import RAMResponseCommands
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.ram.responses import ReadAnyResponse

data_ok: dict = {
    'nadr': 0,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 90,
    'pData': [10, 20, 30, 40, 1, 12],
    'dpa': b'\x00\x00\x04\x82\x00\x00\x00\x5a\x0a\x14\x1e\x28\x01\x0c'
}

data_ok_1: dict = {
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'pData': [10, 20, 30, 40, 1, 12],
    'dpa': b'\x00\x00\x04\x82\x02\x04\x00\x5a\x0a\x14\x1e\x28\x01\x0c'
}

data_error: dict = {
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 4,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x04\x82\x04\x04\x04\x23'
}


class ReadResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, ReadAnyResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1, ReadAnyResponse.from_dpa(data_ok_1['dpa'])],
        ['from_dpa_error', data_error, ReadAnyResponse.from_dpa(data_error['dpa'])],
    ])
    def test_factory_methods_ok(self, _, response_data, response):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.RAM)
        with self.subTest():
            self.assertEqual(response.pcmd, RAMResponseCommands.READ_ANY)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])

    def test_factory_from_json(self):
        with self.assertRaises(NotImplementedError):
            ReadAnyResponse.from_json(dict())

    @parameterized.expand([
        ['from_dpa', data_ok['pData'], ReadAnyResponse.from_dpa(data_ok['dpa'])],
        ['from_dpa', data_ok_1['pData'], ReadAnyResponse.from_dpa(data_ok_1['dpa'])],
    ])
    def test_get_data(self, _, data, response: ReadAnyResponse):
        self.assertEqual(response.data, data)

    @parameterized.expand([
        ['from_dpa_error', ReadAnyResponse.from_dpa(data_error['dpa'])]
    ])
    def test_get_data_error(self, _, response: ReadAnyResponse):
        self.assertIsNone(response.data)

