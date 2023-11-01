import unittest
from iqrfpy.peripherals.os.requests.restart import RestartRequest


class RestartRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = RestartRequest(nadr=2, msgid='restartTest')
        self.dpa = b'\x02\x00\x02\x08\xff\xff'
        self.json = {
            'mType': 'iqrfEmbedOs_Restart',
            'data': {
                'msgId': 'restartTest',
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
