import unittest
from iqrfpy.peripherals.sensor.requests.enumerate import EnumerateRequest


class EnumerateRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = EnumerateRequest(nadr=1, msgid='enumerateTest')
        self.dpa = b'\x01\x00\x5e\x3e\xff\xff'
        self.json = {
            'mType': 'iqrfSensor_Enumerate',
            'data': {
                'msgId': 'enumerateTest',
                'req': {
                    'nAdr': 1,
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
