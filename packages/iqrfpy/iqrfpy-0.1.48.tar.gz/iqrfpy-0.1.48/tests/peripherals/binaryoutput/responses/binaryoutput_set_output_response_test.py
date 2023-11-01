import unittest
from typing import List
from parameterized import parameterized
from iqrfpy.enums.commands import BinaryOutputResponseCommands
from iqrfpy.enums.message_types import BinaryOutputMessages
from iqrfpy.enums.peripherals import Standards
from iqrfpy.peripherals.binaryoutput.responses.set_output import SetOutputResponse
from iqrfpy.response_factory import ResponseFactory
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': BinaryOutputMessages.SET_OUTPUT,
    'msgid': 'setOutputTest',
    'nadr': 3,
    'hwpid': 65535,
    'rcode': 0,
    'dpa_value': 71,
    'result': {
        'prevVals': [True] + [False] * 31
    },
    'dpa': b'\x03\x00\x4b\x80\xff\xff\x00\x47\x01\x00\x00\x00'
}

data_ok1: dict = {
    'mtype': BinaryOutputMessages.SET_OUTPUT,
    'msgid': 'setOutputTest',
    'nadr': 3,
    'hwpid': 65535,
    'rcode': 0,
    'dpa_value': 71,
    'result': {
        'prevVals': [False] * 32
    },
    'dpa': b'\x03\x00\x4b\x80\xff\xff\x00\x47\x00\x00\x00\x00'
}

data_error: dict = {
    'mtype': BinaryOutputMessages.SET_OUTPUT,
    'msgid': 'setOutputTest',
    'nadr': 0,
    'hwpid': 1028,
    'rcode': 3,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x4b\x80\x04\x04\x03\x23'
}


class SetOutputResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        [
            'from_dpa',
            data_ok,
            ResponseFactory.get_response_from_dpa(data_ok['dpa']),
            False
        ],
        [
            'from_dpa',
            data_ok1,
            ResponseFactory.get_response_from_dpa(data_ok1['dpa']),
            False
        ],
        [
            'from_json',
            data_ok,
            ResponseFactory.get_response_from_json(generate_json_response(data_ok)),
            True
        ],
        [
            'from_json',
            data_ok1,
            ResponseFactory.get_response_from_json(generate_json_response(data_ok1)),
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
            self.assertEqual(response.pcmd, BinaryOutputResponseCommands.SET_OUTPUT)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, BinaryOutputMessages.SET_OUTPUT)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    @parameterized.expand([
        [
            'from_dpa',
            data_ok['result']['prevVals'],
            ResponseFactory.get_response_from_dpa(data_ok['dpa']),
        ],
        [
            'from_dpa',
            data_ok1['result']['prevVals'],
            ResponseFactory.get_response_from_dpa(data_ok1['dpa']),
        ],
        [
            'from_json',
            data_ok['result']['prevVals'],
            ResponseFactory.get_response_from_json(generate_json_response(data_ok)),
        ],
        [
            'from_json',
            data_ok1['result']['prevVals'],
            ResponseFactory.get_response_from_json(generate_json_response(data_ok1)),
        ],
    ])
    def test_get_states(self, _, states: List[bool], response: SetOutputResponse):
        self.assertEqual(response.states, states)

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
    def test_get_count_error(self, _, response: SetOutputResponse):
        self.assertIsNone(response.states)
