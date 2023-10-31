import unittest
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.peripherals.os.requests.rfpgm import RfpgmRequest


class RfpgmRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.request = RfpgmRequest(nadr=2, msgid='rfpgmTest')
        self.dpa = b'\x02\x00\x02\x03\xff\xff'
        self.json = {
            'mType': OSMessages.RFPGM.value,
            'data': {
                'msgId': 'rfpgmTest',
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
