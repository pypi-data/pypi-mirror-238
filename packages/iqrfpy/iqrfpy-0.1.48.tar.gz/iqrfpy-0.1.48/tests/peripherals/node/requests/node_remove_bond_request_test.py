import unittest
from iqrfpy.peripherals.node.requests.remove_bond import RemoveBondRequest


class RemoveBondRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = RemoveBondRequest(nadr=1, msgid='removeBondRequest')
        self.dpa = b'\x01\x00\x01\x01\xff\xff'
        self.json = {
            'mType': 'iqrfEmbedNode_RemoveBond',
            'data': {
                'msgId': 'removeBondRequest',
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
