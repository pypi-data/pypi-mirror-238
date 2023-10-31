import unittest
from iqrfpy.peripherals.io.requests.get import GetRequest


class GetRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = GetRequest(nadr=0, msgid='getTest')
        self.dpa = b'\x00\x00\x09\x02\xff\xff'
        self.json = {
            'mType': 'iqrfEmbedIo_Get',
            'data': {
                'msgId': 'getTest',
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
