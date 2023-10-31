import unittest
from iqrfpy.peripherals.os.requests.reset import ResetRequest


class ResetRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = ResetRequest(nadr=2, msgid='resetTest')
        self.dpa = b'\x02\x00\x02\x01\xff\xff'
        self.json = {
            'mType': 'iqrfEmbedOs_Reset',
            'data': {
                'msgId': 'resetTest',
                'req': {
                    'nAdr': 2,
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
