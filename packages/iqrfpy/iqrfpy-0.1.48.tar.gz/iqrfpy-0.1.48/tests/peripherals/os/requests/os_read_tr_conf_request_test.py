import unittest
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.peripherals.os.requests.read_tr_conf import ReadTrConfRequest


class ReadTrConfRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = ReadTrConfRequest(nadr=2, msgid='readTrConfTest')
        self.dpa = b'\x02\x00\x02\x02\xff\xff'
        self.json = {
            'mType': OSMessages.READ_CFG.value,
            'data': {
                'msgId': 'readTrConfTest',
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
