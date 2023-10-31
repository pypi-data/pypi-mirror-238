import unittest
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.node.requests.backup import BackupRequest


class BackupRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x01\x06\xff\xff\x00'
        self.json = {
            'mType': 'iqrfEmbedNode_Backup',
            'data': {
                'msgId': 'backupTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'index': 0
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        ['index', 1, 10, b'\x01\x00\x01\x06\xff\xff\x0a'],
        ['index', 1, 170, b'\x01\x00\x01\x06\xff\xff\xaa'],
    ])
    def test_to_dpa(self, _, nadr: int, index: int, expected):
        request = BackupRequest(nadr=nadr, index=index)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        ['index', 1, 10],
        ['index', 1, 170]
    ])
    def test_to_json(self, _, nadr: int, index: int):
        request = BackupRequest(nadr=nadr, index=index, msgid='backupTest')
        self.json['data']['req']['param']['index'] = index
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [10, b'\x01\x00\x01\x06\xff\xff\x0a'],
        [170, b'\x01\x00\x01\x06\xff\xff\xaa']
    ])
    def test_set_index(self, index, dpa):
        request = BackupRequest(nadr=1, index=0, msgid='backupTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.index = index
        self.json['data']['req']['param']['index'] = index
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_construct_invalid(self, index):
        with self.assertRaises(RequestParameterInvalidValueError):
            BackupRequest(nadr=1, index=index)
