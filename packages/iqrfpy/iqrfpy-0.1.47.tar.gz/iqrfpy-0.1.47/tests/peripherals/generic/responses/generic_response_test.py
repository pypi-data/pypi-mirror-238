import unittest
from typing import List, Optional
from parameterized import parameterized
from iqrfpy.response_factory import ResponseFactory


class GenericResponseTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.json = {
            'mType': 'iqrfRaw',
            'data': {
                'msgId': 'test',
                'rsp': {
                    'rData': ''
                },
                'status': 0
            }
        }

    @parameterized.expand([
        [
            16,
            160,
            3,
            0,
            0,
            55,
            None,
            b'\x10\x00\xa0\x03\x00\x00\x00\x37',
        ],
        [
            62,
            177,
            3,
            5122,
            0,
            55,
            [1, 2, 3],
            b'\x3e\x00\xb1\x03\x02\x14\x00\x37\x01\x02\x03',
        ],
    ])
    def test_from_dpa(self, nadr: int, pnum: int, pcmd: int, hwpid: int, rcode: int, dpa_value: int,
                      pdata: Optional[List[int]], dpa: bytes):
        response = ResponseFactory.get_response_from_dpa(dpa=dpa, allow_generic=True)
        with self.subTest():
            self.assertEqual(response.nadr, nadr)
        with self.subTest():
            self.assertEqual(response.pnum, pnum)
        with self.subTest():
            self.assertEqual(response.pcmd, pcmd)
        with self.subTest():
            self.assertEqual(response.hwpid, hwpid)
        with self.subTest():
            self.assertEqual(response.rcode, rcode)
        with self.subTest():
            self.assertEqual(response.dpa_value, dpa_value)
        with self.subTest():
            self.assertEqual(response.pdata, pdata)

    @parameterized.expand([
        [
            16,
            160,
            3,
            0,
            0,
            55,
            None,
            '10.00.a0.03.00.00.00.37',
        ],
        [
            62,
            177,
            3,
            5122,
            0,
            55,
            [1, 2, 3],
            '3e.00.b1.03.02.14.00.37.01.02.03',
        ],
    ])
    def test_from_json(self, nadr: int, pnum: int, pcmd: int, hwpid: int, rcode: int, dpa_value: int,
                       pdata: Optional[List[int]], rdata: str):
        self.json['data']['rsp']['rData'] = rdata
        response = ResponseFactory.get_response_from_json(json=self.json)
        with self.subTest():
            self.assertEqual(response.nadr, nadr)
        with self.subTest():
            self.assertEqual(response.pnum, pnum)
        with self.subTest():
            self.assertEqual(response.pcmd, pcmd)
        with self.subTest():
            self.assertEqual(response.hwpid, hwpid)
        with self.subTest():
            self.assertEqual(response.rcode, rcode)
        with self.subTest():
            self.assertEqual(response.dpa_value, dpa_value)
        with self.subTest():
            self.assertEqual(response.pdata, pdata)
