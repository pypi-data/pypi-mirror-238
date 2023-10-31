import unittest
from iqrfpy.peripherals.node.requests.read import ReadRequest


class ReadRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = ReadRequest(nadr=1, msgid='readRequest')
        self.dpa = b'\x01\x00\x01\x00\xff\xff'
        self.json = {
            'mType': 'iqrfEmbedNode_Read',
            'data': {
                'msgId': 'readRequest',
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
