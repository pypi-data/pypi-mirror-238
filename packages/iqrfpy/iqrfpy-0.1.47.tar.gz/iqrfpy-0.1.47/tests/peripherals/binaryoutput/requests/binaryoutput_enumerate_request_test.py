import unittest
from iqrfpy.peripherals.binaryoutput.requests.enumerate import EnumerateRequest
from iqrfpy.enums.message_types import BinaryOutputMessages


class EnumerateRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = EnumerateRequest(nadr=3, msgid='enumerateTest')
        self.dpa = b'\x03\x00\x4b\x3e\xff\xff'
        self.json = {
            'mType': BinaryOutputMessages.ENUMERATE.value,
            'data': {
                'msgId': 'enumerateTest',
                'req': {
                    'nAdr': 3,
                    'hwpId': 65535,
                    'param': {},
                },
                'returnVerbose': True
            },
        }

    def test_to_dpa(self):
        self.assertEqual(
            self.request.to_dpa(),
            self.dpa
        )

    def test_to_json(self):
        self.assertEqual(
            self.request.to_json(),
            self.json
        )
