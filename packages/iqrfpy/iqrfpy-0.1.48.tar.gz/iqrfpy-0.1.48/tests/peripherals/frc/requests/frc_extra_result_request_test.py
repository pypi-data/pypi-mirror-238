import unittest
from iqrfpy.peripherals.frc.requests.extra_result import ExtraResultRequest


class ExtraResultRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = ExtraResultRequest(nadr=0, msgid='extraResultTest')
        self.dpa = b'\x00\x00\x0d\x01\xff\xff'
        self.json = {
            'mType': 'iqrfEmbedFrc_ExtraResult',
            'data': {
                'msgId': 'extraResultTest',
                'req': {
                    'nAdr': 0,
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
