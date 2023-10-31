import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import BinaryOutputResponseCommands
from iqrfpy.enums.message_types import BinaryOutputMessages
from iqrfpy.enums.peripherals import Standards
from iqrfpy.peripherals.binaryoutput.responses.enumerate import EnumerateResponse
from iqrfpy.response_factory import ResponseFactory
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': BinaryOutputMessages.ENUMERATE,
    'msgid': 'enumerateTest',
    'nadr': 3,
    'hwpid': 65535,
    'rcode': 0,
    'dpa_value': 71,
    'result': {
        'binOuts': 3
    },
    'dpa': b'\x03\x00\x4b\xbe\xff\xff\x00\x47\x03'
}

data_error: dict = {
    'mtype': BinaryOutputMessages.ENUMERATE,
    'msgid': 'enumerateTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 3,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x4b\xbe\x04\x04\x03\x23'
}


class EnumerateResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        [
            'from_dpa',
            data_ok,
            ResponseFactory.get_response_from_dpa(data_ok['dpa']),
            False
        ],
        [
            'from_json',
            data_ok,
            ResponseFactory.get_response_from_json(generate_json_response(data_ok)),
            True
        ],
        [
            'from_dpa_error',
            data_error,
            ResponseFactory.get_response_from_dpa(data_error['dpa']),
            False
        ],
        [
            'from_json_error',
            data_error,
            ResponseFactory.get_response_from_json(generate_json_response(data_error)),
            True
        ],
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, Standards.BINARY_OUTPUT)
        with self.subTest():
            self.assertEqual(response.pcmd, BinaryOutputResponseCommands.ENUMERATE_OUTPUTS)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, BinaryOutputMessages.ENUMERATE)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    @parameterized.expand([
        [
            'from_dpa',
            data_ok['result']['binOuts'],
            ResponseFactory.get_response_from_dpa(data_ok['dpa']),
        ],
        [
            'from_json',
            data_ok['result']['binOuts'],
            ResponseFactory.get_response_from_json(generate_json_response(data_ok)),
        ],
    ])
    def test_get_count(self, _, count: int, response: EnumerateResponse):
        self.assertEqual(response.count, count)

    @parameterized.expand([
        [
            'from_dpa_error',
            ResponseFactory.get_response_from_dpa(data_error['dpa']),
        ],
        [
            'from_json_error',
            ResponseFactory.get_response_from_json(generate_json_response(data_error)),
        ],
    ])
    def test_get_count_error(self, _, response: EnumerateResponse):
        self.assertIsNone(response.count)
