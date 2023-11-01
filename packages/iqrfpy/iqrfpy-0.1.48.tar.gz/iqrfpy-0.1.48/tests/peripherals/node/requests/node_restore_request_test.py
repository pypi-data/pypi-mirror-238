import random
import unittest
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.node.requests.restore import RestoreRequest


class RestoreRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x01\x00\x01\x07\xff\xff\x8d\x6c\x51\xab\x6a\xf0\xf7\xc8\x3d\x50\x36\x5e\x26\xe1\x3d\x5a\x46\x83' \
                   b'\x20\xbc\xd5\x23\x62\x74\x00\xf5\x80\xe2\xb4\x63\xa6\xad\xdf\xb8\x5a\x79\xad\xf4\x12\x5b\x55\x06' \
                   b'\xa9\x17\xea\x1b\xe1\x29\x06'
        self.json = {
            'mType': 'iqrfEmbedNode_Restore',
            'data': {
                'msgId': 'restoreTest',
                'req': {
                    'nAdr': 1,
                    'hwpId': 65535,
                    'param': {
                        'backupData': [
                            141,
                            108,
                            81,
                            171,
                            106,
                            240,
                            247,
                            200,
                            61,
                            80,
                            54,
                            94,
                            38,
                            225,
                            61,
                            90,
                            70,
                            131,
                            32,
                            188,
                            213,
                            35,
                            98,
                            116,
                            0,
                            245,
                            128,
                            226,
                            180,
                            99,
                            166,
                            173,
                            223,
                            184,
                            90,
                            121,
                            173,
                            244,
                            18,
                            91,
                            85,
                            6,
                            169,
                            23,
                            234,
                            27,
                            225,
                            41,
                            6
                        ]
                    }
                },
                'returnVerbose': True
            }
        }

    def test_to_dpa(self):
        backup_data = random.sample(range(0, 255), 49)
        expected = bytes(b'\x01\x00\x01\x07\xff\xff' + bytes(backup_data))
        request = RestoreRequest(nadr=1, backup_data=backup_data)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    def test_to_json(self):
        backup_data = random.sample(range(0, 255), 49)
        request = RestoreRequest(nadr=1, backup_data=backup_data, msgid='restoreTest')
        self.json['data']['req']['param']['backupData'] = backup_data
        self.assertEqual(
            request.to_json(),
            self.json
        )

    def test_set_backup_data(self):
        request = RestoreRequest(nadr=1, backup_data=self.json['data']['req']['param']['backupData'], msgid='restoreTest')
        print(request.to_dpa())
        print(self.dpa)
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        backup_data = random.sample(range(0, 255), 49)
        dpa = bytes(b'\x01\x00\x01\x07\xff\xff' + bytes(backup_data))
        request.backup_data = backup_data
        self.json['data']['req']['param']['backupData'] = backup_data
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [[0] * 60],
        [[-255]],
        [[256]]
    ])
    def test_construct_invalid(self, backup_data):
        with self.assertRaises(RequestParameterInvalidValueError):
            RestoreRequest(nadr=1, backup_data=backup_data)
